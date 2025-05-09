# matches_calendar/management/commands/update_matches.py
import os

from django.core.management.base import BaseCommand
from matches_calendar.utils import update_matches_from_remote_repo

class Command(BaseCommand):
    help = "Update matches from the remote parsed_json folder in the football_calendar_project repository"

    def handle(self, *args, **options):
        repo_url = "https://github.com/walele993/football_calendar_project.git"
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            self.stderr.write(self.style.ERROR("MONGO_URI environment variable is not set."))
            return

        message = update_matches_from_remote_repo(repo_url=repo_url, mongo_uri=mongo_uri)
        self.stdout.write(self.style.SUCCESS(message))
