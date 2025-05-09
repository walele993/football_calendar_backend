import os
import os
import sys

# Aggiungi la cartella del modulo 'matches_calendar' al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from matches_calendar.utils import update_matches_from_remote_repo


def main():
    repo_url = "https://github.com/walele993/football_calendar_project.git"
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        print("Error: MONGO_URI environment variable is not set.")
        return

    message = update_matches_from_remote_repo(repo_url=repo_url, mongo_uri=mongo_uri)
    print(message)

if __name__ == "__main__":
    main()
