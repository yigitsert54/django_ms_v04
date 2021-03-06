# Generated by Django 3.2.8 on 2022-01-06 12:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=200, null=True)),
                ('answer', models.CharField(blank=True, max_length=1000, null=True)),
                ('topics', models.ManyToManyField(blank=True, to='helpcenter.Topic')),
            ],
            options={
                'ordering': ['question'],
            },
        ),
    ]
