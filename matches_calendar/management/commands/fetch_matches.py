from django.core.management.base import BaseCommand
from matches_calendar.utils import fetch_and_update_matches

class Command(BaseCommand):
    help = 'Fetch and update match data from GitHub'

    def handle(self, *args, **kwargs):
        message = fetch_and_update_matches()
        self.stdout.write(self.style.SUCCESS(message))
