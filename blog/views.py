from django.shortcuts import render
from django.http import HttpResponse
# Create your views here
posts = [ 
    {
        'author':'Jebez Oswald',
        'title':'Blog post 1',
        'content':'First post content',
        'date_posted':'6 June 2025'
    },
    {
        'author' : 'Jethro',
        'title':'Blog post 2',
        'content':'Second post contet',
        'date_posted':'7 June 2025'
    }
]
def home(request):
    context = {
        'posts':posts
    }
    return render(HttpResponse,'blog/home.html',context)

def about(request):
    return render(HttpResponse,'blog/about.html')