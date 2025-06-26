from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST': # the data is sent via POST HTTP request
        form = UserRegisterForm(request.POST)
        if form.is_valid():# backend check
            form.save() # save the user
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You can login now')#display that the accoutn is created
            # redirecting to home page
            return redirect('login') # we redirect to login page
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})


# profile for user

@login_required
def profile(request):
    return render(request,'users/profile.html')

