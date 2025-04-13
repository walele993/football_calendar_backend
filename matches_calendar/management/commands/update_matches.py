# matches_calendar/management/commands/update_matches.py
from django.core.management.base import BaseCommand
from matches_calendar.utils import update_matches_from_json_folder

class Command(BaseCommand):
    help = "Update matches from JSON files in the parsed_json folder"

    def handle(self, *args, **options):
        message = update_matches_from_json_folder(folder='parsed_json')
        self.stdout.write(self.style.SUCCESS(message))
