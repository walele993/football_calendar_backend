from django.urls import path
from .views import MatchListView, MatchDetailView, MatchListFromLocalFile

urlpatterns = [
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
    path('matches-from-local/', MatchListFromLocalFile.as_view(), name='match-list-local'),
]
