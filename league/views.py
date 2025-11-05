from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from league.models import Team, Match, Player, StartingEleven, Substitutes
from league.forms import PlayerForm
from league.match_forms import MatchForm
from league.lineup_forms import StartingElevenForm, SubstitutesForm
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

@login_required
@user_passes_test(lambda u: u.role == 'coach')
def manage_lineup(request, match_pk):
    match = get_object_or_404(Match, pk=match_pk)
    team = request.user.team

    if match.home_team != team and match.away_team != team:
        return HttpResponse("You can only manage lineups for your team's matches.", status=403)

    if request.method == 'POST':
        starting_eleven_form = StartingElevenForm(request.POST, team=team)
        substitutes_form = SubstitutesForm(request.POST, team=team)

        if starting_eleven_form.is_valid() and substitutes_form.is_valid():
            # Clear existing lineup for this match and team
            StartingEleven.objects.filter(match=match, player__team=team).delete()
            Substitutes.objects.filter(match=match, player__team=team).delete()

            # Save new starting eleven
            for player in starting_eleven_form.cleaned_data['players']:
                StartingEleven.objects.create(match=match, player=player)

            # Save new substitutes
            for player in substitutes_form.cleaned_data['players']:
                Substitutes.objects.create(match=match, player=player)

            return redirect('matchday_results', md=match.matchday)
    else:
        current_starting_eleven = StartingEleven.objects.filter(match=match, player__team=team).values_list('player__pk', flat=True)
        current_substitutes = Substitutes.objects.filter(match=match, player__team=team).values_list('player__pk', flat=True)

        starting_eleven_form = StartingElevenForm(initial={'players': list(current_starting_eleven)}, team=team)
        substitutes_form = SubstitutesForm(initial={'players': list(current_substitutes)}, team=team)

    return render(request, 'league/manage_lineup.html', {
        'match': match,
        'team': team,
        'starting_eleven_form': starting_eleven_form,
        'substitutes_form': substitutes_form
    })