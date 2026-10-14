from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

#every models (tables) that we create in python is a subclass of django.db.models.Model
class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # many to one relationship between Post and User models 
    # if the user is deleted then all the objects with this author will also be deleted (cascade delete)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    # sentence embedding used for semantic search (see blog/semantic.py)
    embedding = models.JSONField(null=True, blank=True, editable=False)
    # short extractive summary of long posts (see blog/summary.py); empty for short posts
    summary = models.TextField(blank=True, editable=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # reverse function returns the full url in string format
        return reverse('post-detail',kwargs={'pk':self.pk})



class Tag(models.Model):
    # tags are generated automatically from the post text (see blog/ml.py)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    # set by the toxicity model (see blog/moderation.py); held comments stay hidden from other visitors
    toxicity = models.FloatField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        return f'{self.author} on {self.post}'
