from django import forms
from django.forms import ModelForm
from .models import Support


class SupportForm(ModelForm):
    class Meta:
        model = Support
        fields = ["subject", "question"]
        labels = {
            "subject": "Betreff",
            "question": "Deine Frage",
        }

    def __init__(self, *args, **kwargs):
        super(SupportForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

            if name == "subject":
                field.widget.attrs.update(
                    {"placeholder": "Hier Betreff eingeben"})
            elif name == "question":
                field.widget.attrs.update(
                    {"placeholder": "Hier kannst du uns deine Frage stellen"})
