from django.shortcuts import render, redirect

import markdown2

from . import util
from .forms import ContentForm


def index(request):
    """List of all available wiki entries."""
    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            return redirect("index")
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


def create_page(request):
    """
    Create a new page.
    This function should be removed as this violates REST methodology
    and serve this pupose from '/' endpoint instead.
    """
    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            title = request.POST["title"].lower()
            content = request.POST["content"]
            util.save_entry(title, content)
            return redirect("display_entry", title=title)
    else:
        form = ContentForm()
    return render(request, "encyclopedia/create_page.html", {
        "form": form
    })
