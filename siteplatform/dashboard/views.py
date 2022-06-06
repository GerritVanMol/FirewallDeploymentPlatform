from multiprocessing import context
from urllib import response
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import CreateUserForm, UserForm


# Create your views here.
def loginPage (request):
    messages.info(request, "")
    form = UserForm()#render form
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            form = UserForm()
            return HttpResponseRedirect("dashboard")
        else:             
            messages.error(request, "Username or password incorrect!")
            form = UserForm()
    
    context = { "form":form }
    return render(request, "login.html", context)



def registrationPage (request):
    form = CreateUserForm()#render form

    if request.method == "POST":
        form = CreateUserForm(request.POST)#post form input
        if form.is_valid():#validate
            form.save()
            messages.success(request, "Registration successfull for " + form.cleaned_data.get("username"))
            form = CreateUserForm()#Clear form input
            return HttpResponseRedirect('dashboard')#redirect
            
    context = { "form":form }
    return render(request, "register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


def dashPage(request):
    return render (request, "dash.html", { })