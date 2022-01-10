from django.db import models
from accounts.models import Account
import uuid


# Each Model is a table in the database
# null=True means, it is not required
# blank=True is for the form, it means we are allowed to submit a form with this field empty


class Topic(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["name"]


class Question(models.Model):
    question = models.CharField(max_length=200, null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    topics = models.ManyToManyField("Topic", blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ["question"]


class Support(models.Model):
    owner = models.ForeignKey(
        Account, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, null=False, blank=True)
    question = models.TextField(null=False, blank=True)
    answer = models.TextField(null=True, blank=True)
    answered = models.BooleanField(blank=True, default=False)
    seen = models.BooleanField(blank=True, default=False)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = ["seen", "answered", "created"]
