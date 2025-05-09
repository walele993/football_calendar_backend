import os
import glob
import json
import shutil
import stat
import subprocess
import time
import re
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def on_rm_error(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        logger.error(f"Failed to remove {path}: {e}")


def is_season_valid(filename, min_season_start=2024):
    match = re.match(r"\((\d{4})_\d{2}\)", os.path.basename(filename))
    if match:
        year = int(match.group(1))
        return year >= min_season_start
    return False


def update_matches_from_remote_repo(repo_url, branch='main', folder='parsed_json', mongo_uri=None):
    if not mongo_uri:
        raise ValueError("Missing MongoDB URI")

    start_time = time.time()
    temp_dir = 'temp_repo'

    client = MongoClient(mongo_uri)
    db = client["football_calendar"]
    matches_col = db["matches"]

    logger.info("Starting match update process...")
    logger.info(f"Repository: {repo_url}")
    logger.info(f"Branch: {branch}")
    logger.info(f"Target folder inside repo: {folder}")

    # Cleanup temp repo
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, onerror=on_rm_error)

    try:
        subprocess.run(['git', 'clone', '--depth', '1', '-b', branch, repo_url, temp_dir], check=True)
    except Exception as e:
        logger.error(f"Error cloning repository: {e}")
        return

    parsed_json_path = os.path.join(temp_dir, folder)
    if not os.path.exists(parsed_json_path):
        logger.error(f"Folder '{folder}' not found in the cloned repo.")
        return

    json_files = [f for f in glob.glob(os.path.join(parsed_json_path, '*.json')) if is_season_valid(f)]
    logger.info(f"Found {len(json_files)} valid .json files.")

    inserted = 0
    updated = 0

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load JSON file {json_file}: {e}")
            continue

        league_name = data.get("league", "Unknown League")
        season = data.get("season", "Unknown Season")
        matchdays = data.get("matchdays", [])

        for md in matchdays:
            md_name = md.get("matchday", "Unknown Matchday")
            matches = md.get("matches", [])

            for m in matches:
                date_str = m.get("date")
                time_str = m.get("time", "00:00")
                try:
                    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                except:
                    dt = None

                result = m.get("result", {})
                score_home, score_away = None, None
                if isinstance(result, dict):
                    full_time = result.get("full_time")
                    if full_time and '-' in full_time:
                        try:
                            score_home, score_away = map(int, full_time.split('-'))
                        except:
                            pass

                home_team = m.get("home_team")
                away_team = m.get("away_team")

                match_doc = {
                    "date": dt.strftime("%Y-%m-%d") if dt else None,
                    "time": dt.strftime("%H:%M:%S") if dt else None,
                    "matchday": md_name,
                    "season": season,
                    "is_cancelled": m.get("cancelled", False),
                    "score_home": score_home,
                    "score_away": score_away,
                    "home_team": {"id": hash(home_team) % 10000, "name": home_team},
                    "away_team": {"id": hash(away_team) % 10000, "name": away_team},
                    "league": {"id": hash(league_name) % 10000, "name": league_name},
                }

                query = {
                    "home_team.name": home_team,
                    "away_team.name": away_team,
                    "season": season,
                    "matchday": md_name,
                    "league.name": league_name
                }

                existing = matches_col.find_one(query)
                if existing:
                    matches_col.update_one({"_id": existing["_id"]}, {"$set": match_doc})
                    updated += 1
                else:
                    matches_col.insert_one(match_doc)
                    inserted += 1

    # Cleanup
    try:
        shutil.rmtree(temp_dir, onerror=on_rm_error)
    except Exception as e:
        logger.warning(f"Failed to delete temp dir: {e}")

    logger.info(f"Update completed in {round(time.time() - start_time, 2)}s")
    logger.info(f"Inserted: {inserted}, Updated: {updated}")
    return "MongoDB update completed."
