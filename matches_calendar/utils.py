import os
import glob
import json
from datetime import datetime
from matches_calendar.models import Team, Match

def update_matches_from_json_folder(folder='parsed_json'):
    """
    Reads all JSON files in the specified folder (each containing data for a competition/season)
    and updates the database accordingly.
    The unique match is determined by the combination of matchday, home_team, and away_team.
    """
    json_files = glob.glob(os.path.join(folder, '*.json'))
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Cannot load {json_file}: {e}")
            continue

        # Extract league, season, and matchdays from the JSON
        league = data.get("league", "Unknown League")
        season = data.get("season", "Unknown Season")
        matchdays = data.get("matchdays", [])
        
        for md in matchdays:
            md_name = md.get("matchday", "Unknown Matchday")
            matches = md.get("matches", [])
            for match_data in matches:
                date_str = match_data.get("date")
                time_str = match_data.get("time")
                home_team_name = match_data.get("home_team")
                away_team_name = match_data.get("away_team")
                result = match_data.get("result", {})

                # Combine date and time if available.
                try:
                    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                except Exception as e:
                    print(f"[DEBUG] Error parsing datetime for match {home_team_name} vs {away_team_name}: {e}")
                    dt = None

                # Parse score from result's full_time field if exists.
                score_home = None
                score_away = None
                if isinstance(result, dict):
                    full_time = result.get("full_time")
                    if full_time:
                        try:
                            score_home, score_away = map(int, full_time.split('-'))
                        except Exception as e:
                            print(f"[DEBUG] Error parsing score for {home_team_name} vs {away_team_name}: {e}")
                            score_home, score_away = None, None

                # Get or create the team instances.
                home_team, _ = Team.objects.get_or_create(name=home_team_name)
                away_team, _ = Team.objects.get_or_create(name=away_team_name)

                # Update or create the match based on unique combination of matchday, home_team, and away_team.
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
                    print(f"[INFO] Created match: {home_team_name} vs {away_team_name} on {md_name}")
                else:
                    print(f"[INFO] Updated match: {home_team_name} vs {away_team_name} on {md_name}")
                    
    return "Matches updated from JSON folder successfully!"
