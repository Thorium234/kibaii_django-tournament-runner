from django import forms
from .models import Match, Player, StartingEleven, Substitutes

class StartingElevenForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = StartingEleven
        fields = ['players']

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        if team:
            self.fields['players'].queryset = Player.objects.filter(team=team)

class SubstitutesForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Substitutes
        fields = ['players']

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        if team:
            self.fields['players'].queryset = Player.objects.filter(team=team)
