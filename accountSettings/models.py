# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accountProfile.models import UserProfile


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class OCR(models.TextChoices):
        NATIVE = 'native', 'Native OCR'
        EASY_OCR = 'easyocr', 'EasyOCR'

    darkMode = models.BooleanField(default=False)
    ocrRecognition = models.CharField(
        max_length=10,
        choices=OCR.choices,
        default=OCR.NATIVE,
    )
    saveToCalendar = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)
    instance.profile.save()