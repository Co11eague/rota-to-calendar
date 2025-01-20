from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('name', 'email')  # Customize the list display
	readonly_fields = ('name', 'email', 'message', 'file', 'helpType')  # Make all fields read-only

	def has_add_permission(self, request):
		"""Disable the add button."""
		return False

	def has_change_permission(self, request, obj=None):
		"""Prevent editing of objects."""
		return False