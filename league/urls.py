from django.urls import path
from . import views

urlpatterns = [
    path('', views.league_table, name='league_table'),
    path('matchday/<int:md>/', views.matchday_results, name='matchday_results'),
    path('simulate/', views.simulate_view, name='simulate'),
    path('manage_team/', views.manage_team, name='manage_team'),
    path('manage_team/player/add/', views.player_create, name='player_create'),
    path('manage_team/player/<int:pk>/edit/', views.player_update, name='player_update'),
    path('manage_team/player/<int:pk>/delete/', views.player_delete, name='player_delete'),
    path('matches/', views.match_list, name='match_list'),
    path('matches/add/', views.match_create, name='match_create'),
    path('matches/<int:pk>/edit/', views.match_update, name='match_update'),
    path('matches/<int:pk>/delete/', views.match_delete, name='match_delete'),
    path('matches/<int:match_pk>/manage_lineup/', views.manage_lineup, name='manage_lineup'),
]
