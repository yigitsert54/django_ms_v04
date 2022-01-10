from django.contrib import admin

# Register your models here.
from .models import Match, Bet

admin.site.register(Match)
admin.site.register(Bet)
