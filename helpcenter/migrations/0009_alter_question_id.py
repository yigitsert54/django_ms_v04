# Generated by Django 3.2.8 on 2022-01-09 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpcenter', '0008_alter_question_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.CharField(max_length=500, primary_key=True, serialize=False),
        ),
    ]