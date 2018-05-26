from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import *
from ERP.serializers.serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from ERP.custom_views.common_functions import *
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import  settings
from django.urls import reverse

row_per_page=settings.GLOBAL_SETTINGS['row_per_page']
@api_view(['GET', 'POST'])
def warehouse_create(request):
    if request.method == 'GET':
        return Response({'data':'', 'module':'warehouse'}, template_name='ERP/master/warehouse/create_update.html')
    else:
        serializer = WareHouseSerializer(data=request.data)
        if serializer.is_valid():
            user_id= session_user_id(request)
            date_modified=store_date_time()
            serializer.save(created_by=user_id,created_date=date_modified)
            if request.accepted_renderer.format == 'html':
                return Response({"success_data": "Data added successfully"}, template_name='ERP/master/warehouse/create_update.html')
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
                return Response({"error_data": data}, template_name='ERP/master/warehouse/create_update.html')
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST','Delete'])
#@permission_classes((IsAuthenticated, ))
def warehouse_view(request, id):
    data_obj = WareHouse.objects.get(id=id)
    if request.method == "GET":
        ser_data = WareHouseSerializer(data_obj).data
        if request.accepted_renderer.format == 'html':
            return Response({"data": ser_data,"view_mode":1}, template_name='ERP/master/warehouse/create_update.html')
        return Response({"data": ser_data,"view_mode":1}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST','Delete'])
#@permission_classes((IsAuthenticated, ))
def warehouse_update(request, id):
    data_obj = WareHouse.objects.get(id=id)
    if request.method == "GET":
        ser_data = WareHouseSerializer(data_obj).data
        if request.accepted_renderer.format == 'html':
            return Response({"data": ser_data}, template_name='ERP/master/warehouse/create_update.html')
        return Response({"data": ser_data}, status=status.HTTP_200_OK)
    else:
        serializer = WareHouseSerializer(data_obj, data=request.data, partial=True)
        if serializer.is_valid():
            user_id= session_user_id(request)
            date_modified=store_date_time()
            #return Response({"data": date_modified}, template_name='ERP/master/test.html')
            serializer.save(modified_date=date_modified,modified_by=user_id)
            if request.accepted_renderer.format == 'html':
                return HttpResponseRedirect(reverse('ERP:list_warehouse'))
                #return Response({"data": "Customer Updated successfully"}, template_name='quenchadmin/create_customer.html')
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
                return Response({"error_data": data}, template_name='ERP/master/warehouse/create_update.html') 
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



def delete_warehouse(request,id):
    selected_values=WareHouse.objects.get(pk=id)
    user_id= session_user_id(request)
    date_modified=store_date_time()
    selected_values.modified_date=date_modified
    selected_values.modified_by=user_id
    selected_values.deleted=1
    selected_values.save();
    return HttpResponseRedirect(reverse('ERP:list_warehouse'))


@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def list_warehouse(request):
     custom_filter={}
     custom_filter['deleted']=0
     try:
        if request.data['warehouse_name']:
            custom_filter['warehouse_name']=request.data['warehouse_name']
        if request.data['company']:
            custom_filter['company']=request.data['company']
     except:
        pass
     model_obj = WareHouse.objects.filter(**custom_filter)
     model_data = WareHouseSerializer(model_obj, many=True).data
     page = request.GET.get('page', 1)
     paginator = Paginator(model_data, row_per_page)
     try:
        model_data = paginator.page(page)
     except PageNotAnInteger:
        model_data = paginator.page(1)
     except EmptyPage:
        model_data = paginator.page(paginator.num_pages)
     if request.accepted_renderer.format == 'html':
        return Response({"data": model_data,'module':'warehouse',"custom_filter":custom_filter}, template_name='ERP/master/warehouse/list.html')
     return Response({"data": model_data,"custom_filter":custom_filter}, status=status.HTTP_200_OK)

