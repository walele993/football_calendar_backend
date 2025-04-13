from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    competition = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    matchday = models.CharField(max_length=50, null=True, blank=True)  

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"
    

