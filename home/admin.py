from django.contrib import admin

from .models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
	list_display = ('title', 'order')
	list_editable = ('order',)
# Register your models here.
