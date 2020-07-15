from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import random
import markdown2

from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(label = "Search")

class CreatePageForm(forms.Form):
    title = forms.CharField(label = "Title:")
    content = forms.CharField(label = "Content:", widget=forms.Textarea)

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm
    })

def error(request, message):
    return render(request, "encyclopedia/error.html", {
        "message": message,
        "form": NewSearchForm
    })

def wiki(request, title):
    if util.get_entry(title) is None:
        return redirect("encyclopedia:error", message = "404: Page not found!")
    result = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/page.html", {
        "entries": result,
        "title": title,
        "form": NewSearchForm
    })

def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            if util.get_entry(search) is None:
                search_result = util.list_entries_advanced(search)
                return render(request, "encyclopedia/searchresult.html", {
                            "title": search,
                            "search": search_result,
                            "form": NewSearchForm
                            })
            return redirect("encyclopedia:entry", title = search)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm
    })

def createPage(request):
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if form.is_valid():
            class Submit:
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
            if util.get_entry(Submit.title) is not None:
                return render(request, "encyclopedia/createpage.html", {
                            "form": NewSearchForm,
                            "createPageForm": CreatePageForm,
                            "message": "Page already exist!"
                 })
            else:
                util.save_entry(Submit.title, Submit.content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': Submit.title})) 
    return render(request, "encyclopedia/createpage.html", {
        "form": NewSearchForm,
        "createPageForm": CreatePageForm
    })

def editPage(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title, new_content)
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title})) 
    EditPageForm.initial = content
    return render(request, "encyclopedia/editpage.html", {
        "form": NewSearchForm,
        "editPageForm": EditPageForm(initial={'content': content}),
        "title": title
    })

def randomPage(request):
    array = util.list_entries()
    print(array)
    id = random.randint(0,int(len(array))-1)
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': array[id]}))





