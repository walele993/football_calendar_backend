from django.core.management.base import BaseCommand
from matches_calendar.models import Match

class Command(BaseCommand):
    help = 'Delete all matches from the database.'

    def handle(self, *args, **options):
        total = Match.objects.count()
        Match.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {total} matches from the database.'))
