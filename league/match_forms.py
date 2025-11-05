from django import forms
from .models import Match

class MatchForm(forms.ModelForm):
    RESULT_CHOICES = [
        ('home', 'Home Team Wins'),
        ('away', 'Away Team Wins'),
        ('draw', 'Draw'),
        ('none', 'Not Played Yet'),
    ]
    result = forms.ChoiceField(choices=RESULT_CHOICES, required=False, initial='none')

    class Meta:
        model = Match
        fields = ['home_team', 'away_team', 'matchday', 'venue', 'played']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.played:
            if self.instance.home_score > self.instance.away_score:
                self.fields['result'].initial = 'home'
            elif self.instance.home_score < self.instance.away_score:
                self.fields['result'].initial = 'away'
            else:
                self.fields['result'].initial = 'draw'
        else:
            self.fields['result'].initial = 'none'
