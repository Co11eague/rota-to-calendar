# Create your models here.
from django.db import models


class Contact(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField()
	message = models.TextField()

	def __str__(self):
		return self.name


class FineTune(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField()
	message = models.TextField()
	file = models.FileField(upload_to='fine_tuning/')

	def __str__(self):
		return self.name
