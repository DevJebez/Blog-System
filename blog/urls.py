from django.contrib import admin
from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView, PostDeleteView, UserPostListView, TagPostListView
urlpatterns = [
    path('',PostListView.as_view(),name="blog-home"),
    path('user/<str:username>/',UserPostListView.as_view(),name='user-posts'),
    path('tag/<str:name>/',TagPostListView.as_view(),name='tag-posts'),
    path('post/<int:pk>/comment/',views.add_comment,name='comment-create'),
    path('comment/<int:pk>/delete/',views.delete_comment,name='comment-delete'),
    path('search/',views.search,name='blog-search'),
    path('about/',views.about,name='blog-about'),
    # we use a variable in the url , we use pk = primary key  because that's Django convention for DetailView
    # this checks for blog/post_detail.html automatically 
    path('post/<int:pk>/', PostDetailView.as_view(),name = 'post-detail'),
    path('post/new/',PostCreateView.as_view(),name = 'post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name = "post-update"),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name = 'post-delete')
]
# <app>/<model_name>_<viewtype>.html
