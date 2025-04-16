from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    matchday = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True)
    home_team = models.ForeignKey(Team, related_name="home_matches", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_matches", on_delete=models.CASCADE)
    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, default=None)
    season = models.CharField(max_length=255, null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.competition.name})"
