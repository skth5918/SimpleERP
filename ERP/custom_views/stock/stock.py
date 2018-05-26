from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import masters,stock
from ERP.serializers.serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from ERP.custom_views.common_functions import *
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import  settings
from django.urls import reverse
from rest_framework import status
from django.template.loader import render_to_string
from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import masters,stock
from ERP.serializers.serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from ERP.custom_views.common_functions import *
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import  settings
from django.urls import reverse
from rest_framework import status
from django.template.loader import render_to_string
#from pip._vendor.requests.api import request



def stock_create_update(item,qty,warehouse,company,mode,ref_id,ref_type,ref_name,request):
    '''
    called places
    1.stockentry
       ref_type=1   
    '''
    data = []
    custom_filter={}
    custom_filter['deleted']=0
    custom_filter['item']=item.id
    custom_filter['warehouse']=warehouse.id
    custom_filter['company']=company.id
    stock=Stock.objects.filter(**custom_filter)
    data=[]
    if not stock:
        stock_data={
                "item":item.id,
                "company":company.id,
                "warehouse":warehouse.id,
                "current_stock":qty,
                "blocked_stock":0,
                }
        serializer = StockSerializer(data=stock_data)
        if serializer.is_valid():
            serializer.save()
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
       
    else:
         
        pk=stock[0].id
        stock_selecct=Stock.objects.get(pk=pk)
        current_stock=stock_selecct.current_stock
        blocked_stock=stock_selecct.blocked_stock
        #mode ->1 stock in, #mode-2 stock out
        if mode==1:
            current_stock_new=current_stock+qty
        elif mode==2:
            current_stock=current_stock-qty
        stock_selecct.current_stock=current_stock_new
        stock_selecct=stock_selecct.save()
        
    # add stock tracking
    data_stock_tracking={
                "item":item.id,
                "qty":qty,
                "ref_type":ref_type,
                "ref_id":ref_id,
                "company":company.id,
                "ref_name":ref_name,
                "warehouse" :warehouse.id,
                }
    serializer = Stock_TrackingSerializer(data=data_stock_tracking)
    if serializer.is_valid():
        user_id= session_user_id(request)
        date_modified=store_date_time()
        serializer.save(created_by=user_id,created_date=date_modified)
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
    #return error_details
    

        

@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, ))
def stock_list(request):
    custom_filter = {}
    custom_filter['deleted'] = 0
    try:
        if request.data['item']:
            custom_filter['item'] = request.data['item']
        if request.data['warehouse']:
            custom_filter['warehouse'] = request.data['warehouse']

        if request.data['quantity_stock']:
            custom_filter['quantity_stock'] = request.data['quantity_stock']
    except:
        pass
    model_obj = Stock.objects.filter(**custom_filter)
    model_data = StockSerializer(model_obj, many=True).data
    page = request.GET.get('page', 1)
    paginator = Paginator(model_data, 10)
    try:
        model_data = paginator.page(page)
    except PageNotAnInteger:
        model_data = paginator.page(1)
    except EmptyPage:
        model_data = paginator.page(paginator.num_pages)
    if request.accepted_renderer.format == 'html':
        return Response({"data": model_data, 'module': 'Stock', "custom_filter": custom_filter},
                        template_name='ERP/stock/stocklist.html')
    return Response({"data": model_data, "custom_filter": custom_filter}, status=status.HTTP_200_OK)