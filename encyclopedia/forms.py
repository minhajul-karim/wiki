from django import forms
from django.core.exceptions import ValidationError

from . import util


def pageExists(title):
    """Page existence validation."""
    files = util.list_entries()
    if title in files:
        raise ValidationError("Page already exists")
    else:
        return title


class ContentForm(forms.Form):
    """Form to create a new page."""
    title = forms.CharField(max_length=100,
                            validators=[pageExists])
    content = forms.CharField(widget=forms.Textarea)


class EditContentForm(forms.Form):
    """Form to edit a page."""
    content = forms.CharField(widget=forms.Textarea)
