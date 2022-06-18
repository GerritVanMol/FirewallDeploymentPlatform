from email.policy import default
from logging import PlaceHolder
from random import choices
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"", "placeholder":"Username", "id":"username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"", "placeholder":"Email", "id":"email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"", "placeholder":"Password", "id":"password1"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"", "placeholder":"Comfirm password", "id":"password2"}))
    class Meta:
        model = User;
        fields = ['username', 'email', 'password1', 'password2']

class UserForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"", "placeholder":"Username", "id":"username"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"", "placeholder":"Password", "id":"password1"}))
    class Meta:
        model = User;
        fields = ['username', 'password1']


class CreateFirewallForm(ModelForm):
    premise_code = forms.CharField(widget=forms.TextInput(attrs={"class":"", "placeholder":"e.g. BXL-012", "id":"premise_code"}))
    hostname = forms.CharField(widget=forms.TextInput(attrs={"class":"", "placeholder":"e.g. NMS-FW1", "id":"hostname"}))
    mgmt_ip = forms.GenericIPAddressField()
    class Meta:
        model = Firewalls
        fields = ['premise_code', 'hostname', 'mgmt_ip', 'vendor', 'state', 'configuration_file']
