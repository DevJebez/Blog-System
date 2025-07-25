from django.db import models
from PIL import Image
# Create your models here.

# The default user model doesn't have profile model so we extend user model 
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # this is the profile picture of the user
    img = models.ImageField(upload_to='profile_pics',blank=True, null =True) # profile_pics is the folder where the profile pictures are stored
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call parent save

        if self.img:  # Only proceed if an image was uploaded
            try:
                img = Image.open(self.img.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.img.path)
            except Exception as e:
                print(f"Error processing image: {e}")

            
    