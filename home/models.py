from django.db import models

class Slider(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='slider_images/')
    order = models.PositiveIntegerField(default=0)  # Optional: For ordering slides

    class Meta:
        ordering = ['order']  # Order by the 'order' field in ascending order

    def __str__(self):
        return self.title or f"Slide {self.id}"
# Create your models here.
