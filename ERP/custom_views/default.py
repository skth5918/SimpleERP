from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import *
from ERP.serializers.serializers import *
from django.contrib.auth import authenticate, login, logout
from ERP.custom_views.common_functions import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index(request):
	#return HttpResponse(request.session['_auth_user_id'])
	return render(request, template_name='ERP/master/index.html')


def login_user(request):
	if request.method == 'GET':
		return render(request, 'ERP/login.html')
	else:
		username = request.POST['username']
		password = request.POST['password']
		logout(request)
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['newvariable']='test'
				return HttpResponseRedirect('/erp/home/')
		return render(request, 'ERP/login.html')


def signup_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/erp/home/')
	else:
		form = UserCreationForm()
	return render(request, 'ERP/signup.html', {'form': form})