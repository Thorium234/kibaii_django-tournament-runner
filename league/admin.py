from django.contrib import admin
from .models import Team, Match, Player, StartingEleven, Substitutes

admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(StartingEleven)
admin.site.register(Substitutes)