# Create your models here.
from django.db import models


class Contact(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField()
	message = models.TextField()
	file = models.FileField(upload_to='fine_tuning/', blank=True)

	def __str__(self):
		return self.name

	class Help(models.TextChoices):
		GENERAL = 'general', 'General'
		FINE_TUNING = 'fine-tuning', 'Fine-tuning'

	helpType = models.CharField(
		max_length=15,
		choices=Help.choices,
		default=Help.GENERAL,
	)
