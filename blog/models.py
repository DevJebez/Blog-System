from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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

