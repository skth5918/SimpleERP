from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import *
from ERP.serializers.serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from datetime import datetime

def session_user_id(request):
	user=request.session['_auth_user_id']
	user_id= User.objects.get(id=1)
	return user_id

def session_user_company(request):
	user=request.session['_auth_user_id']
	company_det=Company.objects.get(pk=1)
	return company_det

def store_date_time():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def db_store_date(date):
	#d = datetime.datetime.strptime(date, '%d-%m-%Y')
	#
	#return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	return datetime.strptime(date, '%d-%m-%Y').strftime( "%Y-%m-%d %H:%M:%S")
	#datetime.date.strftime(date, "%Y-%m-%d")

def serires_values(company_id,series_for):
	custom_filter={}
	data=[]
	if company_id:
		custom_filter['company_id']=company_id
	if series_for:
		custom_filter['series_for']=series_for
	series_val=Series.objects.filter(**custom_filter)
	serial_no_return=""
	if series_val:
		series_count=int(series_val[0].series_count)+int(1)
		series_prefix=series_val[0].series_prefix
		id=series_val[0].id
		series_count=str(series_count)
		length=len(series_count);
		zero_count=5-length;
		zero_count_val=0
		if zero_count>0:
			zero_count_val="0"*zero_count
		serial_no_return=str(series_prefix)+str(zero_count_val)+str(series_count)
		series_det=Series.objects.get(pk=id) 
		if series_det:
			series_det.series_count=series_count
			series_det.save()
	return serial_no_return
       
		
		