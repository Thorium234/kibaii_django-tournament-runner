from django.core.management.base import BaseCommand
from league.models import Team

class Command(BaseCommand):
    help = 'Seeds the database with 20 EPL teams'

    def handle(self, *args, **kwargs):
        teams = [
            'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton & Hove Albion',
            'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Leeds United',
            'Leicester City', 'Liverpool', 'Manchester City', 'Manchester United',
            'Newcastle United', 'Nottingham Forest', 'Southampton', 'Tottenham Hotspur',
            'West Ham United', 'Wolverhampton Wanderers',
        ]

        for team_name in teams:
            Team.objects.get_or_create(name=team_name)

        self.stdout.write(self.style.SUCCESS('Successfully seeded teams.'))
