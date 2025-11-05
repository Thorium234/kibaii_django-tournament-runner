import random
from django.core.management.base import BaseCommand
from django.db import transaction
from league.models import Team, Match
from itertools import permutations

class Command(BaseCommand):
    help = 'Simulates the entire tournament'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Starting tournament simulation...")

        # Reset teams and matches
        Team.objects.all().update(
            played=0, won=0, drawn=0, lost=0, goals_for=0, goals_against=0
        )
        Match.objects.all().delete()

        teams = list(Team.objects.all())
        if len(teams) < 2:
            self.stdout.write(self.style.ERROR("Not enough teams to simulate a tournament."))
            return

        # Generate matches
        matchdays = {}
        all_matches = list(permutations(teams, 2))
        random.shuffle(all_matches)

        num_teams = len(teams)
        num_matchdays = (num_teams - 1) * 2

        for i in range(num_matchdays):
            matchdays[i + 1] = []

        match_counter = {team: 0 for team in teams}

        for home_team, away_team in all_matches:
            for md in range(1, num_matchdays + 1):
                if home_team not in [m.home_team for m in matchdays[md]] + [m.away_team for m in matchdays[md]] and \
                   away_team not in [m.home_team for m in matchdays[md]] + [m.away_team for m in matchdays[md]]:
                    if match_counter[home_team] < num_matchdays and match_counter[away_team] < num_matchdays:
                        match = Match(home_team=home_team, away_team=away_team, matchday=md)
                        matchdays[md].append(match)
                        match_counter[home_team] += 1
                        match_counter[away_team] += 1
                        break
        
        for md_matches in matchdays.values():
            Match.objects.bulk_create(md_matches)

        # Simulate matches
        for match in Match.objects.all():
            home_score = random.randint(0, 5)
            away_score = random.randint(0, 5)

            match.home_score = home_score
            match.away_score = away_score
            match.played = True
            match.save()

            # Update home team stats
            match.home_team.played += 1
            match.home_team.goals_for += home_score
            match.home_team.goals_against += away_score

            # Update away team stats
            match.away_team.played += 1
            match.away_team.goals_for += away_score
            match.away_team.goals_against += home_score

            if home_score > away_score:
                match.home_team.won += 1
                match.away_team.lost += 1
            elif home_score < away_score:
                match.away_team.won += 1
                match.home_team.lost += 1
            else:
                match.home_team.drawn += 1
                match.away_team.drawn += 1

            match.home_team.save()
            match.away_team.save()

        self.stdout.write(self.style.SUCCESS('Successfully simulated tournament.'))
