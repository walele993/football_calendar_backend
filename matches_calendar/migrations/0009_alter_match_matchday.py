# Generated by Django 5.2 on 2025-04-16 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches_calendar', '0008_remove_team_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='matchday',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
