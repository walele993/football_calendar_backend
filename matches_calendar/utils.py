import requests
from datetime import datetime
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
                        match_date = datetime.strptime(f"{match_date_str} {match_time_str}", "%Y-%m-%d %H:%M")
                    except ValueError:
                        continue  # Se la data non è valida, salta questa partita

                    # Estrai i punteggi dal risultato
                    try:
                        score_home, score_away = map(int, full_time_result.split('-'))
                    except ValueError:
                        score_home, score_away = None, None  # Se il punteggio non è valido, lascialo a None

                    # Trova o crea i team
                    home_team, created = Team.objects.get_or_create(name=home_team_name)
                    away_team, created = Team.objects.get_or_create(name=away_team_name)

                    # Verifica se la partita esiste già usando matchday, home_team e away_team
                    match, created = Match.objects.get_or_create(
                        home_team=home_team,
                        away_team=away_team,
                        competition=league,
                        season=season,
                        matchday=matchday.get('name', 'Unknown Matchday')  # Assuming matchday has a 'name'
                    )

                    # Se la partita esiste già, aggiorna i punteggi, orario e data
                    if not created:
                        # Aggiorna solo i punteggi e l'orario se diverso
                        if match.score_home != score_home or match.score_away != score_away:
                            match.score_home = score_home
                            match.score_away = score_away
                        
                        # Se vuoi aggiornare anche l'orario
                        match.date = match_date  # Se la data/ora è cambiata
                        
                        match.save()  # Salva le modifiche

                    # Se la partita è nuova, verrà creata automaticamente da get_or_create()
                    else:
                        print(f"Partita creata: {home_team.name} vs {away_team.name} il {match.date}")

        return "Matches fetched and updated successfully!"
    except requests.RequestException as e:
        return f"Error fetching data: {e}"
