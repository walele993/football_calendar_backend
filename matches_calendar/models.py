from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Competition(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    date = models.DateTimeField(null=True, blank=True)
    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matches')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.competition.name})"
