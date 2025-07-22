from django.db.models.signals import post_save # this is the signal that is sent when a model instance is saved
from django.contrib.auth.models import User # this is the sender of the signal
from django.dispatch import receiver # this is the receiver of the signal
from .models import Profile # this is the model that we want to create when a user is created

#this function must be called when a user is created
@receiver(post_save, sender=User) # this decorator connects the signal to the function
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#this function must be called when a user is created
@receiver(post_save, sender=User) # this decorator connects the signal to the function
def create_profile(sender, instance, **kwargs):
    instance.profile.save() # this ensures that the profile is created when the user is created