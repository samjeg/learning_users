# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileForm

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required



def index(request):
	return render(request, 'basic_app/index.html')

def register(request):
	registered = False

	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			print("user and form valid")
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			print('user saved!')
			profile = profile_form.save(commit=False)
			profile.user = user

			print("request files: %s"%request.FILES)

			if 'picture' in request.FILES:
				print('picture found!')
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:
			print(user_form.errors, profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	print(registered)	

	return render(request, 'basic_app/registration.html', { 'user_form':user_form,
															'profile_form':profile_form,
															'registered':registered })


def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("USER IS NOT ACTIVE")
		else:
			return HttpResponse("login username {} and password {} are not permitted" .format(username, password))
	else:
		return render(request, 'basic_app/login.html', {})


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))



