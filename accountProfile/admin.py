from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accountSettings.models import UserSettings
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = "Profile"
	fk_name = "user"


class UserSettingsInline(admin.StackedInline):
	model = UserSettings
	can_delete = False
	verbose_name_plural = "Settings"
	fk_name = "user"


class CustomUserAdmin(UserAdmin):
	inlines = (UserProfileInline, UserSettingsInline,)

	def get_inline_instances(self, request, obj=None):
		# Display the inline only if the user instance exists
		if not obj:
			return []
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
