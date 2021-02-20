from django.forms import fields, widgets
import markdown2
import random

from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from markdown2 import Markdown
from django.shortcuts import redirect, render
from . import util
from django.urls import reverse

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title your entry", widget=forms.TextInput(attrs={'class':'col-md-3 mb-4 form-control autofocus'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'col-md-6 form-control'}))
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "header": "All entries"
    })

def wikies(request, title):
    if util.get_entry(title):
        query = util.get_entry(title)
        return render(request, "encyclopedia/wiki.html", {
            "entry": markdown2.markdown(query),
            "title": title.upper(),            
        })
    else:
        title = "404 error page"
        return render(request, "encyclopedia/error.html",{
            "title": title.upper()
        })

def searchentry(request):
    j = request.GET.get('q')
    if util.get_entry(j):                
        return HttpResponseRedirect(reverse('title', kwargs={'title':j}))
    else: 
        subStr = []        
        for x in util.list_entries():
            if j.upper() in x.upper():
                subStr.append(x)

        return render(request, "encyclopedia/searchresult.html", {
            "list": subStr,        
            "query": j,
            "header": "Matching entries."
                      
        })
  

def saveEntry(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None :
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('title', kwargs={'title':title}))
            else:
                return render(request, "encyclopedia/newentry.html", {
                    "error": "This entry already exist. Try to create a new one.",
                    "form": form,               
            })
                            
    return render(request, "encyclopedia/newentry.html", {
        "header": "Create a new entrie.",
        "form": NewPageForm()
    })

def edit(request, title):     
    return render(request, "encyclopedia/editentry.html", {
        "header": "Edit this entry as  you like.",
        "editform": NewPageForm(initial= {'title': title, 'content': util.get_entry(title)}),
        "title": title,         
    })

def editform(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]  
            if util.get_entry(title):
                util.save_entry(title, content)
            return HttpResponseRedirect(reverse('title', kwargs={'title': title}))
    
def randomentry(request):

    # Even without this first condition it works just fine.
    if request.method == 'GET':
        random_list = util.list_entries()
        entry = random.choice(random_list)
        if util.get_entry(entry):
            
            # I know this is the same as using HttpResponseRedirect
            return redirect(reverse('title', kwargs={'title': entry}))


# This project was a lot of frustration and fun. ;)  

   
        
          
    
          
                    

 
       
