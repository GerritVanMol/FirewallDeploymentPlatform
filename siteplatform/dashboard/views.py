from urllib import response
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import CreateUserForm

# Create your views here.
def loginPage (request):
    return render(request, "login.html", { })


def registrationPage (request):
    form = CreateUserForm()#render form

    if request.method == "POST":
        form = CreateUserForm(request.POST)#post form input
        if form.is_valid():
            form.save()

    context = { "form":form }
    return render(request, "register.html", context)