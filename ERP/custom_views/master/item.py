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
import json

row_per_page=settings.GLOBAL_SETTINGS['row_per_page']
@api_view(['GET', 'POST'])
def item_create(request):
    if request.method == 'GET':
        return Response({'data':'', 'module':'Item'}, template_name='ERP/master/item/create_update.html')
    else:
        mutable = request.POST._mutable
        request.POST._mutable = True
        #request.POST['item_code'] = 'test data Rengaraj'
        #data= request.data
        #return Response({'data':data, 'module':'Item'}, template_name='ERP/master/item/test.html')

        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            user_id= session_user_id(request)
            date_modified=store_date_time()
            serializer.save(created_by=user_id,created_date=date_modified)
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



@api_view(['GET', 'POST','Delete'])
#@permission_classes((IsAuthenticated, ))
def item_view(request, id):
    data_obj = Item.objects.get(id=id)
    if request.method == "GET":
        ser_data = ItemSerializer(data_obj).data
        if request.accepted_renderer.format == 'html':
            return Response({"data": ser_data,"view_mode":1}, template_name='ERP/master/item/create_update.html')
        return Response({"data": ser_data,"view_mode":1}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST','Delete'])
#@permission_classes((IsAuthenticated, ))
def item_update(request, id):
    data_obj = Item.objects.get(id=id)
    ser_data = ItemSerializer(data_obj).data
    if request.method == "GET":
        if request.accepted_renderer.format == 'html':
            return Response({"data": ser_data, 'module':'Item'}, template_name='ERP/master/item/create_update.html')
        return Response({"data": ser_data, 'module':'Item'}, status=status.HTTP_200_OK)
    else:
        serializer = ItemSerializer(data_obj, data=request.data, partial=True)
        if serializer.is_valid():
            user_id= session_user_id(request)
            date_modified=store_date_time()
            #return Response({"data": date_modified}, template_name='ERP/master/test.html')
            serializer.save(modified_date=date_modified,modified_by=user_id)
            if request.accepted_renderer.format == 'html':
                return HttpResponseRedirect(reverse('ERP:item_list'))
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
                return Response({"error_data": data,"data": ser_data}, template_name='ERP/master/item/create_update.html') 
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



def item_delete(request,id):
    selected_values=Item.objects.get(pk=id)
    user_id= session_user_id(request)
    date_modified=store_date_time()
    selected_values.modified_date=date_modified
    selected_values.modified_by=user_id
    selected_values.deleted=1
    selected_values.save();
    return HttpResponseRedirect(reverse('ERP:item_list'))


@api_view(['GET', 'POST'])
def item_list_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        custom_filter={}
        custom_filter['deleted']=0
        items = Item.objects.filter(**custom_filter)
        results = []
        for item in items:
            
            item_json = {}
            item_json['id'] = item.id
            item_json['label'] = item.item_code +" "+item.name
            item_json['value'] = item.item_code
            item_json['tax_group'] = item.tax_group_id
            taxgroup=TaxGroup.objects.get(id=item.tax_group_id)
            item_json['tax_per'] = taxgroup.tax_per
            
            company_id=session_user_company(request);
            custom_filter_price={}
            custom_filter_price['company_id']=company_id
            custom_filter_price['deleted']=0
            custom_filter_price['item_id']=item.id
            price_det=Price.objects.get(**custom_filter_price)
            if price_det:
                item_json['selling_price'] = price_det.selling_price
                item_json['buying_price'] = price_det.buying_price
                
                
            results.append(item_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def item_list(request):
     custom_filter={}
     custom_filter['deleted']=0
     try:
        if request.data['name']:
            custom_filter['name']=request.data['name']
        
        if request.data['item_code']:
            custom_filter['item_code']=request.data['item_code']
            
        if request.data['group']:
            custom_filter['group']=request.data['group']
            
        if request.data['tax_group']:
            custom_filter['tax_group']=request.data['tax_group']
     except:
        pass
     model_obj = Item.objects.filter(**custom_filter)
     model_data = ItemSerializer(model_obj, many=True).data
     page = request.GET.get('page', 1)
     paginator = Paginator(model_data, row_per_page)
     try:
        model_data = paginator.page(page)
     except PageNotAnInteger:
        model_data = paginator.page(1)
     except EmptyPage:
        model_data = paginator.page(paginator.num_pages)
     if request.accepted_renderer.format == 'html':
        return Response({"data": model_data,'module':'Item',"custom_filter":custom_filter}, template_name='ERP/master/item/list.html')
     return Response({"data": model_data,"custom_filter":custom_filter}, status=status.HTTP_200_OK)

