from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import default_storage

import markdown2

from . import util


def index(request):
    """List of all available wiki entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def display_entry(request, title):
    """Read a file, convert content to HTML, and display."""
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(content),
            "title": title})
    return render(request, "encyclopedia/error.html", {
        "message": "404, Not Found."
    })


def search(request):
    """
    Get the title from the form & collect the list of all files.
    If file exists, redirect to that file or keep appending similar
    file names in a list and display that list.
    """
    if request.method == "POST":
        title = request.POST["q"].lower()
        files = util.list_entries()
        possible_files = []
        for file in files:
            if title == file:
                return redirect("display_entry", title=title)
            elif title in file:
                possible_files.append(file)
        if possible_files:
            return render(request, "encyclopedia/index.html", {
                "entries": possible_files
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "File not found."
            })

    return render(request, "encyclopedia/error.html", {
        "message": "Method not allowed."
    })
