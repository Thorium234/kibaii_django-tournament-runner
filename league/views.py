from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from league.models import Team, Match, Player
from league.forms import PlayerForm
from league.match_forms import MatchForm
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
    players = Player.objects.filter(team=team)
    return render(request, 'league/manage_team.html', {'team': team, 'players': players})

@login_required
@user_passes_test(lambda u: u.role == 'coach')
def player_create(request):
    team = request.user.team
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            player.save()
            return redirect('manage_team')
    else:
        form = PlayerForm()
    return render(request, 'league/player_form.html', {'form': form, 'action': 'Add'})

@login_required
@user_passes_test(lambda u: u.role == 'coach')
def player_update(request, pk):
    player = get_object_or_404(Player, pk=pk, team=request.user.team)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('manage_team')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'league/player_form.html', {'form': form, 'action': 'Edit'})

@login_required
@user_passes_test(lambda u: u.role == 'coach')
def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk, team=request.user.team)
    if request.method == 'POST':
        player.delete()
        return redirect('manage_team')
    return render(request, 'league/player_confirm_delete.html', {'player': player})

@login_required
@user_passes_test(lambda u: u.role == 'official')
def match_list(request):
    matches = Match.objects.all().order_by('matchday', 'home_team__name')
    return render(request, 'league/match_list.html', {'matches': matches})

@login_required
@user_passes_test(lambda u: u.role == 'official')
def match_create(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('match_list')
    else:
        form = MatchForm()
    return render(request, 'league/match_form.html', {'form': form, 'action': 'Add'})

@login_required
@user_passes_test(lambda u: u.role == 'official')
def match_update(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('match_list')
    else:
        form = MatchForm(instance=match)
    return render(request, 'league/match_form.html', {'form': form, 'action': 'Edit'})

@login_required
@user_passes_test(lambda u: u.role == 'official')
def match_delete(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        match.delete()
        return redirect('match_list')
    return render(request, 'league/match_confirm_delete.html', {'match': match})