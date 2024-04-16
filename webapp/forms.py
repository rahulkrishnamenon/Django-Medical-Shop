from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import Record


#Register User
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

#Login User
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

#create record form
class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['medicine_name', 'category']

#update record form
class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['medicine_name', 'category']

