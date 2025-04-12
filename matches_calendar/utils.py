import pytz
import requests
from datetime import datetime
from django.utils import timezone
from matches_calendar.models import Team, Match

def fetch_and_update_matches():
    url = "https://raw.githubusercontent.com/walele993/football_calendar_project/main/all_matches.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # La radice è una lista, quindi possiamo iterare direttamente su di essa
        for season_data in data:  # Itera sulla lista delle stagioni
            league = season_data.get('league', 'Unknown League')
            season = season_data.get('season', 'Unknown Season')
            
            # Itera su ogni matchday
            for matchday in season_data.get('matchdays', []):
                for match_data in matchday.get('matches', []):
                    # Estrai le informazioni dalla partita
                    home_team_name = match_data.get('home_team')
                    away_team_name = match_data.get('away_team')
                    match_date_str = match_data.get('date')
                    match_time_str = match_data.get('time')
                    full_time_result = match_data.get('result', {}).get('full_time')

                    if not home_team_name or not away_team_name or not match_date_str or not match_time_str or not full_time_result:
                        # Se i dati sono incompleti, salta questa partita
                        continue
                    
                    # Converti la data e l'ora in un oggetto datetime
                    try:
                        naive_datetime = datetime.strptime(f"{match_date_str} {match_time_str}", "%Y-%m-%d %H:%M")
                    except ValueError:
                        continue  # Se la data non è valida, salta questa partita

                    # Imposta il fuso orario per il datetime
                    # Ad esempio, se i match sono sempre UTC, usa pytz.utc per la conversione
                    local_tz = pytz.timezone("Europe/Rome")  # Cambia il fuso orario a seconda del tuo caso
                    aware_datetime = local_tz.localize(naive_datetime)

                    # Estrai i punteggi dal risultato
                    try:
                        score_home, score_away = map(int, full_time_result.split('-'))
                    except ValueError:
                        score_home, score_away = None, None  # Se il punteggio non è valido, lascialo a None

                    # Trova o crea i team
                    home_team, created = Team.objects.get_or_create(name=home_team_name)
                    away_team, created = Team.objects.get_or_create(name=away_team_name)

                    # Controlla se la partita esiste già e aggiornala se necessario
                    match, created = Match.objects.update_or_create(
                        home_team=home_team,
                        away_team=away_team,
                        date=aware_datetime,
                        competition=league, 
                        season=season,
                        defaults={
                            'score_home': score_home,
                            'score_away': score_away,
                        }
                    )

        return "Matches fetched and updated successfully!"
    except requests.RequestException as e:
        return f"Error fetching data: {e}"
