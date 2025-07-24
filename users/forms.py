from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# Creating a custom form that inherits the default UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    #configuration setting
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']

#this is used to update user email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

#this is used to update profile pic
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['img']
