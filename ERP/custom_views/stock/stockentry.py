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
from .stock import *

from django.db import connection

#from simple_erp.SimpleERP.ERP.custom_views.common_functions import serires_values
#from simple_erp.SimpleERP.ERP.custom_views.common_functions import session_user_company

row_per_page = settings.GLOBAL_SETTINGS['row_per_page']


@api_view(['GET', 'POST'])
def stockentry_items_create(request):
    if request.method == 'GET':
        return Response({'data':'', 'module':'Stock Entry'}, template_name='ERP/stock/stockentry/create_update.html')
    else:
        mutable = request.POST._mutable
        request.POST._mutable = True
        
        if not request.POST["stockentry_id"]:
            company_id=session_user_company(request);
            series=serires_values(company_id,"SE")
            entry_date=db_store_date(request.POST['entry_date'])
            data={
                "series":series,
                "entry_date":entry_date,
                "purpose":request.POST['purpose'],
                "warehouse_from":request.POST['warehouse_from'],
                "warehouse_to":request.POST['warehouse_from'],
                "description":request.POST['description'],
                }
            serializer = StockEntrySerializer(data=data)
            serializer.is_valid()
            if serializer.is_valid():
                user_id= session_user_id(request)
                date_modified=store_date_time()
                stock_entry=serializer.save(created_by=user_id,created_date=date_modified)
                stockentry_id=stock_entry.id
                
            else:
                stockentry_id=""
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
            stockentry_id=request.POST["stockentry_id"]
        if stockentry_id:
            data_stock_entry_items={
                "stockentry":stockentry_id,
                "item":request.POST['item'],
                "qty":request.POST['qty'],
                "accepted_qty":request.POST['qty'],
                "rejected_qty":0,
                "accepted_status" :1,
                "warehouse_from":request.POST['warehouse_from'],
                "warehouse_to":request.POST['warehouse_from'],

                }
            serializer = Stockentry_itemsSerializer(data=data_stock_entry_items)
            serializer.is_valid()
            if serializer.is_valid():
                user_id= session_user_id(request)
                date_modified=store_date_time()
                company_id=session_user_company(request);
                stockentry_items=serializer.save(created_by=user_id,created_date=date_modified)
                stockentry_items_id=stockentry_items.id
                item_id=request.POST['item']
                item_details=Item.objects.get(pk=item_id)
                
                if item_details.serial:
                    serial_nos=request.POST['serial_nos']
                    serial_nos=serial_nos.strip("")
                    if serial_nos:
                        #pass
                        val=Serial_no_create(1,stockentry_items_id,serial_nos,2,request)
                    else:
                        #pass
                        val=Serial_no_create(1,stockentry_items_id,None,1,request)
        return_data={"stockentry":stockentry_id}
        return Response(return_data)
    
    
def Serial_no_create(ref_type,ref_id,serial_nos,serial_no_mode,request):
    
    if ref_type==1:
        
        stock_items=Stockentry_items.objects.get(pk=ref_id)
        qty=stock_items.qty
        item=stock_items.item_id
        warehouse_from=stock_items.warehouse_from_id
        #return item
        
    if ref_type==2:
        purchase_items=PurchaseInvoice_Items.objects.get(pk=ref_id)
        qty=purchase_items.qty
        item=purchase_items.item_id
        warehouse_from=purchase_items.warehouse_id
        
        
        
    #return "serial_no_mode"
    item_details=Item.objects.get(pk=item)
    data=[]
    serials=[]
    if item_details  and serial_no_mode==1:
        serial_no_count=item_details.serial_no_count
        serial_prefix=item_details.serial_prefix
        serial_no_start=int(serial_no_count)+1
        serial_no_end=int(serial_no_start)+int(qty);
        data_obj=Item.objects.get(pk=item)
        update_data={
            "serial_no_count":serial_no_end-1
            
            }
        item_serializer = ItemSerializer(data_obj, data=update_data, partial=True)
        if item_serializer.is_valid():
           item_serializer.save()
        
        
        for serial_no in range(serial_no_start,serial_no_end):
            serial_no=str(serial_no)
            length=len(serial_no);
            zero_count=8-length;
            zero_count_val=0
            if zero_count>0:
                zero_count_val="0"*zero_count
            serial_no_val=serial_prefix+zero_count_val+serial_no
            data_serial_nos={
            "serial_no":serial_no_val,
            "item":item,
            "status":0,
            "warehouse" :warehouse_from,
            }
            serials.append(data_serial_nos)
        
    if item_details and serial_no_mode==2:
        serial_nos=serial_nos.splitlines()
        for serial_no in serial_nos:
            data_serial_nos={
            "serial_no":serial_no,
            "item":item,
            "status":0,
            "warehouse" :warehouse_from,
            }
            serials.append(data_serial_nos)
    for serials_data in serials:
        serializer = Serial_noSerializer(data=serials_data)
        if serializer.is_valid():
            user_id= session_user_id(request)
            date_modified=store_date_time()
            company_id=session_user_company(request);
            serial_save=serializer.save(created_by=user_id,created_date=date_modified,company=company_id)
            serial_no_id=serial_save.id
            serail_no_tracking(ref_type,ref_id,item,warehouse_from,serial_no_id,"Purchase Invoice Create",request)
            
            
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
    return True

def serail_no_tracking(ref_type,ref_id,item,warehouse_from,serial_no_id,ref_name,request):
    data_serial_nos_tracking={
                "serial_no_id":serial_no_id,
                "ref_type":ref_type,
                "ref_id":ref_id,
                "ref_name":ref_name,
                "item":item,
                "warehouse" :warehouse_from,
                }
    serializer = Serial_no_trackingSerializer(data=data_serial_nos_tracking)
    if serializer.is_valid():
        user_id= session_user_id(request)
        date_modified=store_date_time()
        company_id=session_user_company(request);
        serializer.save(created_by=user_id,created_date=date_modified,company=company_id)
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
            

@api_view(['GET'])
def stockentry_items(request):
    html=None
    if request.is_ajax() and request.GET['id']:
        id=request.GET['id']
        data = []
        custom_filter={}
        custom_filter['deleted']=0
        custom_filter['stockentry_id']=id
        model_obj = Stockentry_items.objects.filter(**custom_filter)
        #data = Stockentry_itemsSerializer(model_obj, many=True).data
        html = render_to_string('ERP/stock/stockentry/stockentry_items.html', {'data': model_obj})
    return HttpResponse(html)

@api_view(['GET'])
def stockentryitems_delete(request):
    if request.is_ajax() and request.GET['id']:
        id=request.GET['id']
        selected_values=Stockentry_items.objects.get(pk=request.GET['id'])
        user_id= session_user_id(request)
        date_modified=store_date_time()
        selected_values.modified_date=date_modified
        selected_values.modified_by=user_id
        selected_values.deleted=1
        selected_values.save();
        with connection.cursor() as cursor:
            query_serial_no_tracking="update ERP_serial_no_tracking set deleted=1 where ref_type=1 and ref_id=%s" %(id)
            cursor.execute(query_serial_no_tracking)
         
            query_serial_no="""update ERP_serial_no set deleted=1 where id in (select serial_no_id_id from ERP_serial_no_tracking where  ref_type=1 
            and ref_id=%s)""" %(id) 
            cursor.execute(query_serial_no)
    return HttpResponse("1")

@api_view(['GET', 'POST'])
def stockentry_create(request):
    data=[]
    if request.method == 'GET':
        return Response({'data':'', 'module':'Stock Entry'}, template_name='ERP/stock/stockentry/create_update.html')
    else:
        if request.POST['stockentry_id']:
            stockentry_id=request.POST['stockentry_id']
            stockentry_submit_confirm(stockentry_id,request)
    if request.accepted_renderer.format == 'html':
                return Response({"error_data": data}, template_name='ERP/stock/stockentry/create_update.html')
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def stockentry_update(request, id):
    data=[]
    if request.method == 'GET':
        data=StockEntry.objects.get(id=id)
        return Response({'data':data, 'module':'Stock Entry'}, template_name='ERP/stock/stockentry/create_update.html')
    else:
        if request.POST['stockentry_id']:
            stockentry_id=request.POST['stockentry_id']
            stockentry_submit_confirm(stockentry_id,request)
    if request.accepted_renderer.format == 'html':
                return Response({"error_data": data}, template_name='ERP/stock/stockentry/create_update.html')
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

def stockentry_submit_confirm(stockentry_id,request):
    stockentry=StockEntry.objects.get(id=stockentry_id)
    if stockentry:
        stockentry.status=1
        stockentry.save()
        stockentryitems_list=Stockentry_items.objects.all().filter(stockentry=stockentry_id,deleted=0)
        for stockentryitems_list_val in stockentryitems_list:
            ref_type=1
            ref_id=stockentryitems_list_val.id
            qty=stockentryitems_list_val.qty
            item=stockentryitems_list_val.item
            warehouse=stockentryitems_list_val.warehouse_from
            company=stockentryitems_list_val.company
            if stockentry.purpose==1:
                ref_name="Stock Create"
                mode=1
                data=stock_create_update(item, qty, warehouse, company, mode, ref_id, ref_type, ref_name,request)
                return HttpResponse(data)
            if stockentry.purpose=="2":
                ref_name="Stock Transfer"
                warehouse_to=stockentryitems_list_val.warehouse_to
                if warehouse_to:
                    warehouse=WareHouse.objects.get(pk=warehouse_to)
                    warehouse_company=warehouse.company
                    
                    #first reduce from store
                    stock_create_update(item, qty, warehouse, company, 2, ref_id, ref_type, ref_name,request)
                    #second added to store
                    stock_create_update(item, qty, warehouse_to, warehouse_company, 1, ref_id, ref_type, ref_name,request)
    

    #return Response({"data": "Stockentry Updated successfully"}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def stockentry_list(request):
    custom_filter={}
    custom_filter['deleted']=0
    try:
        if request.data['name']:
            custom_filter['name']=request.data['name']
        if request.data['customergroup']:
            custom_filter['customergroup']=request.data['customergroup']

        if request.data['primary_contact_no']:
            custom_filter['primary_contact_no']=request.data['primary_contact_no']
    except:
        pass
    model_obj = StockEntry.objects.filter(**custom_filter)
    model_data = StockEntrySerializer(model_obj, many=True).data
    page = request.GET.get('page', 1)
    paginator = Paginator(model_data, row_per_page)
    try:
        model_data = paginator.page(page)
    except PageNotAnInteger:
        model_data = paginator.page(1)
    except EmptyPage:
        model_data = paginator.page(paginator.num_pages)
    if request.accepted_renderer.format == 'html':
        return Response({"data": model_data,'module':'Stock Entry',"custom_filter":custom_filter}, template_name='ERP/stock/stockentry/list.html')
    return Response({"data": model_data,"custom_filter":custom_filter}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST','Delete'])
#@permission_classes((IsAuthenticated, ))
def stockentry_view(request, id):
    if request.method == 'GET':
        data=StockEntry.objects.get(id=id)
        return Response({'data':data, 'module':'Stock Entry'}, template_name='ERP/stock/stockentry/create_update.html')

@api_view(['GET', 'POST','Delete'])
#@permission_classes((IsAuthenticated, ))
def stockentry_delete(request,id):
    selected_values=StockEntry.objects.get(pk=id)
    user_id= session_user_id(request)
    date_modified=store_date_time()
    selected_values.modified_date=date_modified
    selected_values.modified_by=user_id
    selected_values.deleted=1
    selected_values.save();
    #item delete
    with connection.cursor() as cursor:
        query = "update ERP_stockentry_items set deleted=1 where stockentry_id=%s" %(id)
        cursor.execute(query)
        
        query_serial_no_tracking="update ERP_serial_no_tracking set deleted=1 where ref_type=1 and ref_id in (select id from ERP_stockentry_items where  stockentry_id=%s)" %(id)
        cursor.execute(query_serial_no_tracking)
     
        query_serial_no="""update ERP_serial_no set deleted=1 where id in (select serial_no_id_id from ERP_serial_no_tracking where  ref_type=1 
        and ref_id in (select id from ERP_stockentry_items where  stockentry_id=%s) )""" %(id) 
        #serial no tracking deleted
        cursor.execute(query_serial_no)
        
        
    
    
    return HttpResponseRedirect(reverse('ERP:stockentry_list'))