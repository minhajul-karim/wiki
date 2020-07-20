from django import forms
from . import util
from django.core.exceptions import ValidationError


def pageExists(title):
    files = util.list_entries()
    if title in files:
        raise ValidationError("Page already exists")
    else:
        return title


class ContentForm(forms.Form):
    title = forms.CharField(max_length=100, validators=[pageExists])
    content = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Write in Markdown here'}))
