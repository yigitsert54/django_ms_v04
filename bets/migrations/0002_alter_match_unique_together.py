# Generated by Django 3.2.8 on 2021-10-18 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='match',
            unique_together={('league', 'date', 'home_team', 'away_team')},
        ),
    ]
