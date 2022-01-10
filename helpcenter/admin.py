from django.contrib import admin

# Register your models here.
from .models import Topic, Question, Support


admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Support)
