from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)

    @property
    def points(self):
        return (self.won * 3) + self.drawn

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    matchday = models.IntegerField()
    venue = models.CharField(max_length=100, blank=True, null=True)
    played = models.BooleanField(default=False)

    def __str__(self):
        return f"Matchday {self.matchday}: {self.home_team} vs {self.away_team}"

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True) # e.g., 'Goalkeeper', 'Defender', 'Midfielder', 'Forward'

    def __str__(self):
        return f"{self.name} ({self.team.name})"

class StartingEleven(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='starting_eleven')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('match', 'player')

    def __str__(self):
        return f"{self.player.name} in starting eleven for {self.match}"

class Substitutes(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='substitutes')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('match', 'player')

    def __str__(self):
        return f"{self.player.name} is a substitute for {self.match}"