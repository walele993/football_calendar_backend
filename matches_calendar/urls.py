from django.urls import path
from .views import LeagueListView, MatchListView, TeamListView, MatchDetailView, LeagueDetailView, TeamDetailView, MatchListFromLocalFile

urlpatterns = [
    path('leagues/', LeagueListView.as_view(), name='league-list'),
    path('leagues/<int:pk>/', LeagueDetailView.as_view(), name='league-detail'),
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
    path('matches-from-local/', MatchListFromLocalFile.as_view(), name='match-list-local'),
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
]
