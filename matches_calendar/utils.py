import os
import glob
import json
import shutil
import stat
import subprocess
from datetime import datetime
from matches_calendar.models import Team, Match
import logging
import re

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def on_rm_error(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        logger.error(f"Failed to remove {path}: {e}")

def is_season_valid(filename, min_season_start=2022):
    """
    Extracts the starting year from the filename, which is expected to begin with (YYYY-YY),
    and checks if it's >= min_season_start.
    """
    match = re.match(r"\((\d{4})_\d{2}\)", os.path.basename(filename))
    if match:
        year = int(match.group(1))
        return year >= min_season_start
    return False

def update_matches_from_remote_repo(repo_url, branch='main', folder='parsed_json'):
    temp_dir = 'temp_repo'

    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir, onerror=on_rm_error)
        except Exception as e:
            logger.error(f"Error removing existing temp directory: {e}")
            return

    try:
        logger.info(f"Cloning repository from {repo_url} (branch: {branch})...")
        subprocess.run(['git', 'clone', '--depth', '1', '-b', branch, repo_url, temp_dir], check=True)
    except Exception as e:
        logger.error(f"Error cloning repository: {e}")
        return

    all_json_files = glob.glob(os.path.join(temp_dir, folder, '*.json'))

    # 🔍 Filtra solo le stagioni dal 2022-23 in poi
    json_files = [f for f in all_json_files if is_season_valid(f)]

    total_files = len(json_files)
    total_matches = 0
    created_matches = 0
    updated_matches = 0

    if total_files == 0:
        logger.warning(f"No valid JSON files (from 2022-23) found in folder {folder}.")
    
    for json_file in json_files:
        logger.info(f"Processing file: {json_file}")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Cannot load {json_file}: {e}")
            continue

        league = data.get("league", "Unknown League")
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

                try:
                    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                except Exception as e:
                    logger.debug(f"Error parsing datetime for match {home_team_name} vs {away_team_name}: {e}")
                    dt = None

                score_home = None
                score_away = None
                if isinstance(result, dict):
                    full_time = result.get("full_time")
                    if full_time:
                        try:
                            score_home, score_away = map(int, full_time.split('-'))
                        except Exception as e:
                            logger.debug(f"Error parsing score for {home_team_name} vs {away_team_name}: {e}")

                home_team, _ = Team.objects.get_or_create(name=home_team_name)
                away_team, _ = Team.objects.get_or_create(name=away_team_name)

                match, created = Match.objects.update_or_create(
                    matchday=md_name,
                    home_team=home_team,
                    away_team=away_team,
                    defaults={
                        "date": dt,
                        "score_home": score_home,
                        "score_away": score_away,
                        "competition": league,
                        "season": season,
                    }
                )

                if created:
                    created_matches += 1
                    logger.info(f"Created match: {home_team_name} vs {away_team_name} on {md_name}")
                else:
                    updated_matches += 1
                    logger.info(f"Updated match: {home_team_name} vs {away_team_name} on {md_name}")

    try:
        shutil.rmtree(temp_dir, onerror=on_rm_error)
    except Exception as e:
        logger.error(f"Error during cleanup of temporary directory: {e}")

    logger.info(f"Processed {total_files} JSON files, total matches: {total_matches}, created: {created_matches}, updated: {updated_matches}")
    return "Matches updated from remote repository successfully!"
