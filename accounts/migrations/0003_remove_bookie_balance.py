# Generated by Django 3.2.8 on 2021-10-18 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_bookie_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookie',
            name='balance',
        ),
    ]