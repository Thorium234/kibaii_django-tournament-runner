from django.shortcuts import render, redirect
from django.http import HttpResponse
from league.models import Team, Match
from django.core.management import call_command
from django.contrib.auth.decorators import login_required, user_passes_test

def league_table(request):
    teams = Team.objects.all().order_by('-won', '-drawn', '-goals_for') # Simple ordering
    return render(request, 'league/league_table.html', {'teams': teams})

def matchday_results(request, md):
    matches = Match.objects.filter(matchday=md)
    return render(request, 'league/matchday_results.html', {'matches': matches, 'matchday': md})

@login_required
@user_passes_test(lambda u: u.role == 'official')
def simulate_view(request):
    call_command('simulate_tournament')
    return redirect('league_table')

@login_required
@user_passes_test(lambda u: u.role == 'coach')
def manage_team(request):
    team = request.user.team
    return render(request, 'league/manage_team.html', {'team': team})