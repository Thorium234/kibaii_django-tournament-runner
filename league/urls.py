from django.urls import path
from . import views

urlpatterns = [
    path('', views.league_table, name='league_table'),
    path('matchday/<int:md>/', views.matchday_results, name='matchday_results'),
    path('simulate/', views.simulate_view, name='simulate'),
    path('manage_team/', views.manage_team, name='manage_team'),
]
