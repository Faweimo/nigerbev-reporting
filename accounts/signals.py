from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Department, Profile,User

# when a user is created, create instance of Profile and department
@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# save the instance profile after creation
@receiver(post_save, sender=User) 
def save_profile(sender, instance, **kwargs):
        instance.profile.save()