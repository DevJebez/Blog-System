from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST': # the data is sent via POST HTTP request
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username}')#display that the accoutn is created
            # redirecting to home page
            return redirect('blog-home')
    else:
        form = UserCreationForm()
    return render(request,'users/register.html',{'form':form})

