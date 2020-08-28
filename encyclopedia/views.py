import random
import markdown2
from django.shortcuts import render, redirect

from . import util
from .forms import ContentForm, EditContentForm


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
        form = ContentForm(
            initial={"content": "# Page Title\n\nWrite in Markdown here."})
    return render(request, "encyclopedia/create_page.html", {
        "form": form
    })


def edit(request, title):
    """
    Display existing content for GET request.
    Save edited content for POST request.
    """
    if request.method == "POST":
        form = EditContentForm(request.POST)
        if form.is_valid():
            new_content = request.POST["content"]
            util.save_entry(title, new_content)
            return redirect("display_entry", title=title)
    else:
        content = util.get_entry(title)
        form = EditContentForm(initial={
            "content": content
        })
    return render(request, "encyclopedia/edit_page.html", {
        "form": form,
        "title": title
    })


def random_page(request):
    """Displays a random page."""
    files = util.list_entries()
    random_index = random.randint(0, len(files) - 1)
    return redirect("display_entry", title=files[random_index])
