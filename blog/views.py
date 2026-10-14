from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import Post, Tag, Comment
from .ml import related_posts
from .moderation import moderate
from .semantic import semantic_search
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView,CreateView, UpdateView, DeleteView
)
# this gives the "login required" functionality to the class , we import it for PostCreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
# These are functions based views that render the HTML templatess
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
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context

class TagPostListView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs.get('name'))
        return self.tag.posts.order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class PostDetailView(DetailView):
    model = Post 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = related_posts(self.object)
        visible = Q(is_approved=True)
        if self.request.user.is_authenticated:
            # commenters always see their own held comments
            visible |= Q(author=self.request.user)
        context['comments'] = self.object.comments.filter(visible).select_related('author')
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    fields = ['title','content']
    # we override form_valid method 
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post 
    fields = ['title','content']

    # we override form_valid method 
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object() # a method to get the post object 
        if self.request.user == post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object() # a method to get the post object 
        if self.request.user == post.author:
            return True
        return False

@login_required
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get('content', '').strip()[:1000]
    if not content:
        messages.warning(request, 'Your comment is empty.')
        return redirect(post)
    comment = Comment(post=post, author=request.user, content=content)
    if moderate(comment):
        messages.success(request, 'Your comment was posted.')
    else:
        messages.warning(request, 'Your comment was held for review.')
    comment.save()
    return redirect(post)

@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user not in (comment.author, comment.post.author):
        return HttpResponseForbidden()
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect(comment.post)

def search(request):
    query = request.GET.get('q', '').strip()
    results = semantic_search(query) if query else []
    return render(request, 'blog/search.html', {'query': query, 'results': results, 'title': 'Search'})

def about(request):
    return render(request,'blog/about.html')