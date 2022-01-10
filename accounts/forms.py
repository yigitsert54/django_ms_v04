from django import forms
from django.forms import ModelForm
from .models import *


class AddBookieForm(ModelForm):
    class Meta:
        model = Bookie

        fields = ["name", "invested_stake"]
        labels = {
            "name": "Wettanbieter",
            "invested_stake": "Wettkapital in €",
        }

    def __init__(self, *args, **kwargs):
        super(AddBookieForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
            if name == "invested_stake":
                field.widget.attrs.update({"placeholder": 0})


class MoneyForm(ModelForm):
    amount = forms.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Bookie
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        super(MoneyForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
            if name == "amount":
                field.widget.attrs.update({"placeholder": 0})
                field.label = "Betrag"


class AccountForm(ModelForm):
    class Meta:
        model = Account

        fields = ["first_name", "last_name", "email"]
        labels = {
            "first_name": "Vorname",
            "last_name": "Nachname",
            "email": "E-Mail-Adresse"
        }

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})


class NotificationsForm(ModelForm):
    class Meta:
        model = Account
        fields = ["notifications"]
