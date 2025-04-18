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

def is_season_valid(filename, min_season_start=2024):
    match = re.match(r"\((\d{4})_\d{2}\)", os.path.basename(filename))
    if match:
        year = int(match.group(1))
        return year >= min_season_start
    return False

def update_matches_from_remote_repo(repo_url, branch='main', folder='parsed_json'):
    start_time = time.time()
    temp_dir = 'temp_repo'

    logger.info("Starting match update process...")
    logger.info(f"Repository: {repo_url}")
    logger.info(f"Branch: {branch}")
    logger.info(f"Target folder inside repo: {folder}")

    # Step 1: Delete temp repo if exists
    if os.path.exists(temp_dir):
        logger.info("Removing existing temp directory...")
        try:
            shutil.rmtree(temp_dir, onerror=on_rm_error)
        except Exception as e:
            logger.error(f"Error removing temp directory: {e}")
            return

    # Step 2: Clone repo
    try:
        logger.info("Cloning repository...")
        subprocess.run(['git', 'clone', '--depth', '1', '-b', branch, repo_url, temp_dir], check=True)
        logger.info("Clone completed.")
    except Exception as e:
        logger.error(f"Error cloning repository: {e}")
        return

    # Step 3: Check for parsed_json folder
    parsed_json_path = os.path.join(temp_dir, folder)
    if not os.path.exists(parsed_json_path):
        logger.error(f"Folder '{folder}' not found in the cloned repo.")
        return f"Folder '{folder}' not found in the cloned repo."

    all_json_files = glob.glob(os.path.join(parsed_json_path, '*.json'))
    logger.info(f"Found {len(all_json_files)} .json files in '{folder}'.")

    json_files = [f for f in all_json_files if is_season_valid(f)]
    logger.info(f"Valid JSON files (from 2023 onwards): {len(json_files)}")

    total_files = len(json_files)
    total_matches = 0
    created_matches = 0
    updated_matches = 0

    if total_files == 0:
        logger.warning("No valid JSON files found.")
        return "No valid JSON files found."

    for json_file in json_files:
        logger.info(f"Processing {json_file}")
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

                match, created = Match.objects.get_or_create(
                    matchday=md_name,
                    home_team=home_team,
                    away_team=away_team,
                    league=league,
                    season=season,
                )
                
                if created:
                    # Se il match è stato creato (è un nuovo record), salviamo i dati
                    match.date = dt
                    match.score_home = score_home
                    match.score_away = score_away
                    match.is_cancelled = is_cancelled
                    match.save()  # Salviamo il nuovo match nel database
                    created_matches += 1
                    logger.info(f"Created match: {home_team_name} vs {away_team_name} on {md_name}")
                else:
                    # Se il match esiste già, controlliamo se i dati sono cambiati
                    if (
                        match.date != dt or
                        match.score_home != score_home or
                        match.score_away != score_away or
                        match.is_cancelled != is_cancelled
                    ):
                        # Se i dati sono cambiati, aggiorniamo il record
                        match.date = dt
                        match.score_home = score_home
                        match.score_away = score_away
                        match.is_cancelled = is_cancelled
                        match.save()  # Salviamo l'aggiornamento
                        updated_matches += 1
                        logger.info(f"Updated match: {home_team_name} vs {away_team_name} on {md_name}")
                    else:
                        # Se i dati non sono cambiati, non facciamo nulla
                        logger.info(f"No changes: {home_team_name} vs {away_team_name} on {md_name}")


        logger.info(f"Finished processing {json_file}")

    # Cleanup
    try:
        shutil.rmtree(temp_dir, onerror=on_rm_error)
        logger.info("Temp directory removed.")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

    end_time = time.time()
    logger.info(f"Update complete in {round(end_time - start_time, 2)}s")
    logger.info(f"Files processed: {total_files}")
    logger.info(f"Matches total: {total_matches}, created: {created_matches}, updated: {updated_matches}")

    return "Matches updated successfully!"
