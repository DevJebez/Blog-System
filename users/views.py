from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required #ensures login authentication to acess the profile page
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
# Create your views here.

def register(request):
    if request.method == 'POST': # the data is sent via POST HTTP request
        form = UserRegisterForm(request.POST)
        if form.is_valid():# backend check
            form.save() # save the user
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You can login now')#display that the account is created
            # redirecting to home page
            return redirect('login') # we redirect to login page
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})


# profile for user

@login_required
def profile(request):
    #this handles the user submit button
    if request.method == 'POST':
        # we populate the forms with the respective fields using instance argument 
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated')#display that the profile is updated]
            return redirect('profile') # we redirect to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request,'users/profile.html',context) 

