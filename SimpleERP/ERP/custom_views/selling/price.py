from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import masters,stock,selling
from ERP.serializers.serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from ERP.custom_views.common_functions import *
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import  settings
from django.urls import reverse
from rest_framework import status


row_per_page = settings.GLOBAL_SETTINGS['row_per_page']
@api_view(['GET', 'POST'])
def price_create(request):
    if request.method == 'GET':
        return Response({'data':'', 'module':'Item Price'}, template_name='ERP/selling/price/create_update.html')
    else:
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            user_id = session_user_id(request)
            date_modified = store_date_time()
            serializer.save(created_by=user_id, created_date=date_modified)
            
            priceserializer=PriceLogSerializer(data=request.data)
            if priceserializer.is_valid():
                priceserializer.save(created_by=user_id, created_date=date_modified);
            
            if request.accepted_renderer.format == 'html':
                return Response({"success_data": "Data added successfully"}, template_name='ERP/selling/price/create_update.html')
            return Response({"data": "Data added successfully"}, status=status.HTTP_201_CREATED)
        else:
            error_details = []
            for key in serializer.errors.keys():
                error_details.append({"field": key, "message": serializer.errors[key][0]})
            data = {
            "Error": {
            "status": 400,
            "message": "Your submitted data was not valid - please correct the below errors",
            "error_details": error_details
            }
            }
            if request.accepted_renderer.format == 'html':
                return Response({"error_data": data}, template_name='ERP/selling/price/create_update.html')
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'Delete'])
# @permission_classes((IsAuthenticated, ))
def price_view(request, id):
    data_obj = Price.objects.get(id=id)
    if request.method == "GET":
        ser_data = PriceSerializer(data_obj).data
        if request.accepted_renderer.format == 'html':
            return Response({"data": ser_data, "view_mode":1}, template_name='ERP/selling/price/create_update.html')
        return Response({"data": ser_data, "view_mode":1}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'Delete'])
# @permission_classes((IsAuthenticated, ))
def price_update(request, id):
    data_obj = Price.objects.get(id=id)
    ser_data = PriceSerializer(data_obj).data
    if request.method == "GET":
        if request.accepted_renderer.format == 'html':
            return Response({"data": ser_data, 'module':'Item Price'}, template_name='ERP/selling/price/create_update.html')
        return Response({"data": ser_data, 'module':'Item Size'}, status=status.HTTP_200_OK)
    else:
        serializer = PriceSerializer(data_obj, data=request.data, partial=True)
        if serializer.is_valid():
            user_id = session_user_id(request)
            date_modified = store_date_time()
            # return Response({"data": date_modified}, template_name='ERP/master/test.html')
            serializer.save(modified_date=date_modified, modified_by=user_id)
            priceserializer=PriceLogSerializer(data=request.data)
            if priceserializer.is_valid():
                priceserializer.save(created_by=user_id, created_date=date_modified);
            
            if request.accepted_renderer.format == 'html':
                return HttpResponseRedirect(reverse('ERP:price_list'))
            
            
                # return Response({"data": "Customer Updated successfully"}, template_name='quenchadmin/create_customer.html')
            return Response({"data": "Customer Updated successfully"}, status=status.HTTP_200_OK)
        else:
            error_details = []
            for key in serializer.errors.keys():
                error_details.append({"field": key, "message": serializer.errors[key][0]})
            data = {
                    "Error": {
                        "status": 400,
                        "message": "Your submitted data was not valid - please correct the below errors",
                        "error_details": error_details
                        }
                    }
            if request.accepted_renderer.format == 'html':
                return Response({"error_data": data, "data": ser_data}, template_name='ERP/selling/price/create_update.html') 
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def price_delete(request, id):
    selected_values = Price.objects.get(pk=id)
    user_id = session_user_id(request)
    date_modified = store_date_time()
    selected_values.modified_date = date_modified
    selected_values.modified_by = user_id
    selected_values.deleted = 1
    selected_values.save();
    return HttpResponseRedirect(reverse('ERP:price_list'))


@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, ))
def price_list(request):
     custom_filter = {}
     custom_filter['deleted'] = 0
     try:
        if request.data['item']:
            custom_filter['item'] = request.data['item']
        if request.data['company']:
            custom_filter['company'] = request.data['company']
       
     except:
        pass
     model_obj = Price.objects.filter(**custom_filter)
     model_data = PriceSerializer(model_obj, many=True).data
     page = request.GET.get('page', 1)
     paginator = Paginator(model_data, row_per_page)
     try:
        model_data = paginator.page(page)
     except PageNotAnInteger:
        model_data = paginator.page(1)
     except EmptyPage:
        model_data = paginator.page(paginator.num_pages)
     if request.accepted_renderer.format == 'html':
        return Response({"data": model_data, 'module':'Price', "custom_filter":custom_filter}, template_name='ERP/selling/price/list.html')
     return Response({"data": model_data, "custom_filter":custom_filter}, status=status.HTTP_200_OK)

