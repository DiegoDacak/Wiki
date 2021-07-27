from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import markdown
import secrets

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    data = util.get_entry(entry)
    if data:
        return render(request, "encyclopedia/entry.html", {
            "data": markdown.markdown(data),
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "search": entry
        })
        

def search(request):
    search = request.POST.get('q')
    if util.get_entry(search):
        return HttpResponseRedirect("/wiki/" + search)
    else:
        possible_entries = []
        for value in util.list_entries():
            if search.upper() in value.upper():
                possible_entries.append(value)
        return render(request, "encyclopedia/entry.html", {
            "possible_entries": possible_entries,
            "search": search,
        })

def new_entry(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not util.get_entry(title):
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "data": markdown.markdown(content),
                "entry": title
            })
        else:
            return render(request, "encyclopedia/new_entry.html", {
                "error": "Duplicate entry"
            })
    else: 
        return render(request, "encyclopedia/new_entry.html")

def edit(request, entry):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "data": markdown.markdown(content),
            "entry": title
        })
    else:
        return render(request, "encyclopedia/edit.html", {
            "content": util.get_entry(entry),
            "entry": entry
        })

def random(request):
    entries = util.list_entries()
    entry = secrets.choice(entries)
    data = util.get_entry(entry)
    return render(request, "encyclopedia/entry.html", {
        "data": markdown.markdown(data),
        "entry": entry
    })
