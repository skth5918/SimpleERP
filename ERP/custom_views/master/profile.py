from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import *
from ERP.serializers.serializers import *
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def create(request):
	if request.method == 'GET':
		return Response({'data':'', 'module':'Company'}, template_name='ERP/master/company/create_update_profile.html')
