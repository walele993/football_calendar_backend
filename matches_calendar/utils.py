import os
import glob
import json
import shutil
import stat
import subprocess
import time
from datetime import datetime
from matches_calendar.models import Team, Match, League
import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def on_rm_error(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        logger.error(f"Failed to remove {path}: {e}")

def is_season_valid(filename, min_season_start=2023):
    match = re.match(r"\((\d{4})_\d{2}\)", os.path.basename(filename))
    if match:
        year = int(match.group(1))
        return year >= min_season_start
    return False

def update_matches_from_remote_repo(repo_url, branch='main', folder='parsed_json'):
    start_time = time.time()
    temp_dir = 'temp_repo'

    print("[INFO] Starting match update process...")
    print(f"[INFO] Repository: {repo_url}")
    print(f"[INFO] Branch: {branch}")
    print(f"[INFO] Target folder inside repo: {folder}")

    # Step 1: Delete temp repo if exists
    if os.path.exists(temp_dir):
        print("[INFO] Removing existing temp directory...")
        try:
            shutil.rmtree(temp_dir, onerror=on_rm_error)
        except Exception as e:
            logger.error(f"Error removing temp directory: {e}")
            return

    # Step 2: Clone repo
    try:
        print("[INFO] Cloning repository...")
        subprocess.run(['git', 'clone', '--depth', '1', '-b', branch, repo_url, temp_dir], check=True)
        print("[INFO] Clone completed.")
    except Exception as e:
        logger.error(f"Error cloning repository: {e}")
        return

    # Step 3: Check for parsed_json folder
    parsed_json_path = os.path.join(temp_dir, folder)
    if not os.path.exists(parsed_json_path):
        logger.error(f"Folder '{folder}' not found in the cloned repo.")
        print("[ERROR] Folder not found:", parsed_json_path)
        return f"Folder '{folder}' not found in the cloned repo."

    print("[INFO] Reading JSON files...")
    all_json_files = glob.glob(os.path.join(temp_dir, folder, '*.json'))
    print(f"[INFO] Found {len(all_json_files)} .json files in '{folder}'.")

    json_files = [f for f in all_json_files if is_season_valid(f)]
    print(f"[INFO] Valid JSON files (from 2023 onwards): {len(json_files)}")

    total_files = len(json_files)
    total_matches = 0
    created_matches = 0
    updated_matches = 0

    if total_files == 0:
        logger.warning("No valid JSON files found.")
        return "No valid JSON files found."

    for json_file in json_files:
        print(f"[INFO] Processing {json_file}")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Cannot load {json_file}: {e}")
            continue

        league_name = data.get("league", "Unknown League")
        league, _ = League.objects.get_or_create(name=league_name)

        season = data.get("season", "Unknown Season")
        matchdays = data.get("matchdays", [])

        for md in matchdays:
            md_name = md.get("matchday", "Unknown Matchday")
            matches = md.get("matches", [])

            for match_data in matches:
                total_matches += 1
                date_str = match_data.get("date")
                time_str = match_data.get("time")
                home_team_name = match_data.get("home_team")
                away_team_name = match_data.get("away_team")
                result = match_data.get("result", {})
                is_cancelled = match_data.get("cancelled", False)

                try:
                    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                except Exception:
                    dt = None

                score_home = None
                score_away = None
                if isinstance(result, dict):
                    full_time = result.get("full_time")
                    if full_time:
                        try:
                            score_home, score_away = map(int, full_time.split('-'))
                        except Exception:
                            pass

                home_team, _ = Team.objects.get_or_create(name=home_team_name)
                away_team, _ = Team.objects.get_or_create(name=away_team_name)

                match, created = Match.objects.update_or_create(
                    matchday=md_name,
                    home_team=home_team,
                    away_team=away_team,
                    league=league,
                    season=season,
                    defaults={
                        "date": dt,
                        "score_home": score_home,
                        "score_away": score_away,
                        "is_cancelled": is_cancelled,
                    }
                )

                if created:
                    created_matches += 1
                else:
                    updated_matches += 1

    # Cleanup
    try:
        shutil.rmtree(temp_dir, onerror=on_rm_error)
        print("[INFO] Temp directory removed.")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

    end_time = time.time()
    print(f"[INFO] Update complete in {round(end_time - start_time, 2)}s")
    print(f"[INFO] Files processed: {total_files}")
    print(f"[INFO] Matches total: {total_matches}, created: {created_matches}, updated: {updated_matches}")

    return "Matches updated successfully!"
