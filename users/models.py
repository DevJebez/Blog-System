from django.db import models

# Create your models here.

# The default user model doesn't have profile model so we extend user model 
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # this is the profile picture of the user
    img = models.ImageField(default='default.jpg', upload_to='profile_pics') # profile_pics is the folder where the profile pictures are stored
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs) #parent class save method
        # resizing the image to 300x300 pixels
        from PIL import Image
        img = Image.open(self.img.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.img.path)
            
    