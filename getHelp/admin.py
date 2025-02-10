from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('name', 'email')
	readonly_fields = ('name', 'email', 'message', 'file', 'helpType')

	def has_add_permission(self, request):
		"""Disable the add button."""
		return False

	def has_change_permission(self, request, obj=None):
		"""Prevent editing of objects."""
		return False
