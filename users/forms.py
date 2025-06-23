from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Creating a custom form that inherits the default UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    #configuration setting
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']