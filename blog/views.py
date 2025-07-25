from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView,CreateView
)
# this gives the login functionality to the class , we import for PostCreateView
from django.contrib.auth.mixins import LoginRequiredMixin


'''
ListView uses - <app_label>/<model_name>_list.html
DetailView uses - <app_label/<model_name>_detail.html
CreateView uses - <app_label/model_name>_form.html

'''
'''
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

'''
'''
# These are function based views that render the HTML templatess
def home(request):
    context = {
        'posts': Post.objects.all() # here the Post model is called as posts
    }
    return render(request,'blog/home.html',context)
'''

class PostListView(ListView): 
    model = Post # here the model is called as objects.list 
    template_name = 'blog/home.html' # this is default route <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # we order the query to the database to view the latest ones first
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post 

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    fields = ['title','content']
    # we override form_valid method 
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

def about(request):
    return render(request,'blog/about.html')