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
#from simpleerp.SimpleERP.ERP.models.stock import StockEntry


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
def salesitem_list_autocomplete(request):
    from django.db import connection
    if request.is_ajax():
        q = request.GET.get('term', '')
        with connection.cursor() as cursor:
            query = """Select  item.id as id,item.name as name, item.item_code as item_code,
            item.sales_unit_id as unit,item.tax_group_id  as tax_group_id from 
            ERP_item item where (item.name like '%%%s%%' or item.item_code like '%%%s%%' or 
            item.id in (select item_id from ERP_serial_no where serial_no like '%%%s%%' and deleted=0)) 
            and variants!=1 and deleted=0 """ % (q, q,q)
            cursor.execute(query)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                item_id=row[0]
                item_name=row[1]
                item_code=row[2]
                sales_unit=row[3]
                tax_group_id=row[4]
                mode=1
                try:
                    serial_no_check=Serial_no.objects.get(serial_no=q)
                    if serial_no_check:
                        mode=2
                except:
                    pass
                return_json = {}
                items_details=Item.objects.get(pk=row[0])
                return_json['id'] =item_id
                return_json['name'] =item_name
                return_json['item_code'] = item_code
                return_json['lable'] =item_id
                if mode==1:
                    return_json['value'] =item_name
                    return_json['serial_no'] =""
                elif mode==2:
                    return_json['value'] =q
                    return_json['serial_no'] =q
                else:
                    return_json['value'] =item_name
                
                results.append(return_json)
            '''[
            return_json = {}
            results = []
            return_json['query'] = query'''
            
            data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@api_view(['GET', 'POST'])
def customer_list_autocomplete(request):
    
    if request.is_ajax():
        q = request.GET.get('term', '')
        custom_filter={}
        company_id=session_user_company(request);
        custom_filter['deleted']=0
        custom_filter['company_id']=company_id
        suppliers = Customer.objects.filter(**custom_filter)
        results = []
        for supplier in suppliers:
            return_json = {}
            return_json['id'] = supplier.id
            return_json['label'] = supplier.name +" "+supplier.primary_contact_no
            return_json['value'] = supplier.name
            return_json['company_id'] = supplier.company_id
            results.append(return_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@api_view(['GET', 'POST'])
def supplier_list_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        custom_filter={}
        company_id=session_user_company(request);
        custom_filter['deleted']=0
        custom_filter['company_id']=company_id
        suppliers = Supplier.objects.filter(**custom_filter)
        results = []
        for supplier in suppliers:
            return_json = {}
            return_json['id'] = supplier.id
            return_json['label'] = supplier.name +" "+supplier.primary_contact_no
            return_json['value'] = supplier.name
            return_json['company_id'] = supplier.company_id
            results.append(return_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
