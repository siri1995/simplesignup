from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    IAM_CHOICES = [
        ('agent', 'AGENT'),
        ('buyer', 'BUYER'),
        ('owner', 'OWNER'),
        ('builder', 'BUILDER'),
    ]
    contact_number = models.CharField(max_length=11)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iam_name = models.CharField(max_length= 7)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


