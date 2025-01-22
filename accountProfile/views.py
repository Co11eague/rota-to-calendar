from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from accountProfile.forms import CustomPasswordChangeForm, PersonalDataForm
from accountProfile.models import UserProfile


@login_required
def index(request):
	user = User.objects.get(id=request.user.id)
	user_profile = UserProfile.objects.get(user=request.user)

	# Instantiate the password change form
	if request.method == 'POST' and 'change_password' in request.POST:
		password_form = CustomPasswordChangeForm(user, request.POST)
		accountProfile_form = PersonalDataForm(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'date_of_birth': user_profile.date_of_birth,
                'phone_number': user_profile.phone_number,
                'address': user_profile.address,
                'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None,
            },
            instance=user_profile
        )

		if password_form.is_valid():
			password_form.save()
			update_session_auth_hash(request, password_form.user)  # Keep user logged in after password change
			messages.success(request, 'Your password was successfully updated!')
			return redirect('accountProfile')  # Replace with your actual profile page URL name
		else:
			messages.error(request, 'Please correct the error below.')
	elif request.method == 'POST' and 'update_profile' in request.POST:
		accountProfile_form = PersonalDataForm(request.POST, request.FILES, instance=user_profile)
		password_form = CustomPasswordChangeForm(user)
		if accountProfile_form.is_valid():
			user.first_name = accountProfile_form.cleaned_data['first_name']
			user.last_name = accountProfile_form.cleaned_data['last_name']
			user.email = accountProfile_form.cleaned_data['email']
			user.save()
			accountProfile_form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return redirect('accountProfile')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		password_form = CustomPasswordChangeForm(user)
		accountProfile_form = PersonalDataForm(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'date_of_birth': user_profile.date_of_birth,
                'phone_number': user_profile.phone_number,
                'address': user_profile.address,
                'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None,
            },
            instance=user_profile
        )

	return render(
		request,
		'accountProfile/index.html',
		{
			'user': user,
			'userProfile': user_profile,
			'password_form': password_form,
			'accountProfile_form': accountProfile_form,
		}
	)

# Create your views here.
