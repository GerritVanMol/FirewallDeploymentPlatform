from multiprocessing import context
from telnetlib import STATUS
from urllib import response
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Firewalls

from .forms import CreateUserForm, UserForm
import requests
from bs4 import BeautifulSoup as bs


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
            return redirect("dashboard")
        else:             
            messages.error(request, "Username or password incorrect!")
            form = UserForm()
    
    context = { "form":form }
    return render(request, "dashboard/login.html", context)


def registrationPage (request):
    form = CreateUserForm()#render form

    if request.method == "POST":
        form = CreateUserForm(request.POST)#post form input
        if form.is_valid():#validate
            form.save()
            messages.success(request, "Registration successfull for " + form.cleaned_data.get("username"))
            form = CreateUserForm()#Clear form input
            return redirect('dashboard')#redirect
            
    context = { "form":form }
    return render(request, "dashboard/register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")

#@login_required(login_url='login')
def dashPage(request):
    firewalls = Firewalls.objects.all()
    context = { "firewalls":firewalls}
    return render (request, "dashboard/dash.html", context)


def configurePage(request):
    return render (request, "dashboard/configure.html", { })

def testPage(request):
    return render (request, "dashboard/testing.html", { })


def getFirewallData():
    response = requests.get('https://10.0.89.103/api/?type=keygen&user=admin&password=rfvTGB123',verify=False)
    soup = bs(response.content,'html.parser')
    #store the data inside the <key>element
    key = soup.find('key').text
    cmd = """<show><system><info></info></system></show>"""

    r = requests.get("https://10.0.89.103/api/?type=op&cmd={}&key={}".format(cmd,key),verify=False)
    output = bs(r.content,'html.parser')
    print("The hostname is " + (output.response.result.system.hostname).text)
    print("The management ip address and mask is " + (output.find('ip-address')).text + " " + (output.response.result.system.netmask).text)
    print("The default gateway is " + (output.find('default-gateway')).text)
    print("PAN OS version is " + (output.find('sw-version')).text)