# Generated by Django 3.2.8 on 2021-11-01 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0002_alter_match_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bet',
            options={'ordering': ['-match']},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-date', 'league'], 'verbose_name_plural': 'Matches'},
        ),
    ]
