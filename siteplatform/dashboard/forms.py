from logging import PlaceHolder
from django import forms
from django.forms import ModelForm
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