from django.contrib import admin
from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView, PostDeleteView
urlpatterns = [
    path('',PostListView.as_view(),name="blog-home"),
    path('about/',views.about,name='blog-about'),
    # we use a variable in the url , we use pk = primary key  because that's Django convention for DetailView
    # this checks for blog/post_detail.html automatically 
    path('post/<int:pk>/', PostDetailView.as_view(),name = 'post-detail'),
    path('post/new/',PostCreateView.as_view(),name = 'post-create'),
    path('post/<int:pk>/update',PostUpdateView.as_view(), name = "post-update"),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name = 'post-delete')
]
# <app>/<model_name>_<viewtype>.html
