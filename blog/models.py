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

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # reverse function returns the full url in string format
        return reverse('post-detail',kwargs={'pk':self.pk})

