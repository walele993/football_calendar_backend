from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    matchday = models.CharField(max_length=50)
    season = models.CharField(max_length=20)
    competition = models.CharField(max_length=100)

    date = models.DateTimeField(null=True, blank=True)

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')

    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('matchday', 'season', 'home_team', 'away_team')
        ordering = ['date']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.season} - {self.matchday})"
