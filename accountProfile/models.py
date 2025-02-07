# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	date_of_birth = models.DateField(null=True, blank=True)
	phone_number = models.CharField(max_length=15, null=True, blank=True)
	address = models.TextField(null=True, blank=True)
	profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
	instance.profile.save()
