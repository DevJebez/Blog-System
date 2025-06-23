from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
# Create your views here.
def register(request):
    if request.method == 'POST': # the data is sent via POST HTTP request
        form = UserRegisterForm(request.POST)
        if form.is_valid():# backend check
            form.save() # save the user
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username}!')#display that the accoutn is created
            # redirecting to home page
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

