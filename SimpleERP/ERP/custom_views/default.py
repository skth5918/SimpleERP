from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import *
from ERP.serializers.serializers import *
from django.contrib.auth import authenticate, login, logout
from ERP.custom_views.common_functions import *

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


