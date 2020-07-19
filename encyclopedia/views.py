from django.shortcuts import render
from django.http import HttpResponse

import markdown2

from . import util


def index(request):
    """List of all available wiki entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def display_entry(request, title):
    """Display wiki entry."""
    markdown_content = util.get_entry(title)
    if markdown_content:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(markdown_content),
            "title": title})
    return render(request, "encyclopedia/error.html")
