from django.contrib import admin

# Register your models here.
from .models import Account, Bookie

admin.site.register(Account)
admin.site.register(Bookie)
