# Generated by Django 3.2.8 on 2022-01-09 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpcenter', '0011_support_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='answered',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]