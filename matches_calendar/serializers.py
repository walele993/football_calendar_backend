from django.db import models

# Modello per la Squadra
class Team(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Modello per la Lega
class League(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default="#FFFFFF")  # Colore per la lega

    def __str__(self):
        return self.name

# Modello per la Partita
class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    league = models.ForeignKey(League, related_name='matches', on_delete=models.CASCADE)
    date = models.DateTimeField()
    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} ({self.date})"
