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
from django.db.models import Sum
from django.template.loader import render_to_string

row_per_page = settings.GLOBAL_SETTINGS['row_per_page']
@api_view(['GET', 'POST'])
def sales_create(request):
    if request.method == 'GET':
        return Response({'data':'', 'module':'Sales Create'}, template_name='ERP/selling/sales/create_update.html')
    

@api_view(['GET', 'POST'])
def sales_items(request):
    html=None
    model_obj=[]
    #return Response("Hai")
    if request.is_ajax() and request.GET['id']:
        id=request.GET['id']
        data = []
        #return Response(request.GET['id'])
        custom_filter={}
        custom_filter['deleted']=0
        custom_filter['sales_invoice_id']=id
        
        model_obj = SalesInvoice_Items.objects.filter(**custom_filter).order_by('-id')
        model_obj_invoice = Salesinvoice.objects.get(pk=id)
            
        #data = Stockentry_itemsSerializer(model_obj, many=True).data
    html = render_to_string('ERP/selling/sales/sales_items.html', {'data': model_obj,"basic_data":model_obj_invoice})
    #html = render_to_string('ERP/stock/test.html', {'data': request})
    return HttpResponse(html)

@api_view(['GET', 'POST'])
def items_create(request):
    item_id=request.data['item']
    serial_no=request.data['serial_no']
    sales_invoice_id=request.data['sales_invoice_id']
    error_details=[]
    company_id=session_user_company(request);
    if not sales_invoice_id:
        
        if request.POST['bill_type']==2:
            mode="EST"
        else:
            mode="SIN"
        series=serires_values(company_id,mode)
        sales_date=db_store_date(request.POST['sales_date'])
        data={
                "series":series,
                "sales_date":sales_date,
                "customer":request.POST['customer'],
                "bill_type":request.POST['bill_type'],
                "bill_mode":request.POST['bill_mode'],
                }
        serializer = SalesInvoiceSerializer(data=data)
        
        if serializer.is_valid():
            user_id= session_user_id(request)
            date_modified=store_date_time()
            sales_invoice=serializer.save(created_by=user_id,created_date=date_modified)
            sales_invoice_id=sales_invoice.id
        else:
            purchaseinvoice_id=""
            for key in serializer.errors.keys():
                error_details.append({"field": key, "message": serializer.errors[key][0]})
                data = {
                "Error": {
                "status": 400,
                "message": "Your submitted data was not valid - please correct the below errors",
                "error_details": error_details
                }
                }
    if sales_invoice_id:
       if sales_invoice_id:
            discount=0;
            item=request.POST['item'];
            qty=request.POST['qty']
            item_price=Price.objects.get(item=item,company=company_id,deleted=0)
            rate=item_price.selling_price
            
            tax_group=item_price.selling_tax_group_id
            tax_per=item_price.selling_tax_group.tax_per
            bill_amount=float(qty)*float(rate)
            tax_amount=(float(bill_amount)*float(tax_per/100))
            net_amount=float(tax_amount)+bill_amount;
            bill_amount_before_tax=bill_amount
            
            data_purchaseinvoice_items={
                "sales_invoice":sales_invoice_id,
                "item":request.POST['item'],
                "qty":qty,
                "rate":rate, 
                "bill_amount":bill_amount,
                "discount":discount,
                "bill_amount_before_tax":bill_amount_before_tax,
                "tax_per":tax_per,
                "tax_amount":tax_amount,
                "net_amount":net_amount,
                "taxgroup" :tax_group,
                'deleted':0
                

                }
            serializer = SalesInvoice_ItemsSerializer(data=data_purchaseinvoice_items)
            serializer.is_valid()
            if serializer.is_valid():
                user_id= session_user_id(request)
                date_modified=store_date_time()
                company_id=session_user_company(request);
                salesinvoice_item=serializer.save(company=company_id,created_by=user_id,created_date=date_modified)
                salesinvoice_item_id=salesinvoice_item.id
                item_id=request.POST['item']
                item_details=Item.objects.get(pk=item_id)
                sales_invoice_rate_update(sales_invoice_id)    
            else:
                #purchaseinvoice_id=""
                error_details= []
                for key in serializer.errors.keys():
                    error_details.append({"field": key, "message": serializer.errors[key][0]})
                    data = {
                    "Error": {
                    "status": 400,
                    "message": "Your submitted data was not valid - please correct the below errors",
                    "error_details": error_details
                    }
                    }
                
            return_data={"sales_invoice_id":sales_invoice_id,"error_details":error_details}
    return Response(return_data)

    return Response({'data':"tesst"})


def sales_invoice_rate_update(salesinvoice_id):
    # Rate Updatation
    bill_amount = SalesInvoice_Items.objects.filter(sales_invoice=salesinvoice_id,deleted=0).aggregate(Sum('bill_amount'))
    tax_amount = SalesInvoice_Items.objects.filter(sales_invoice=salesinvoice_id,deleted=0).aggregate(Sum('tax_amount'))
    net_amount = SalesInvoice_Items.objects.filter(sales_invoice=salesinvoice_id,deleted=0).aggregate(Sum('net_amount'))
    item_discount = SalesInvoice_Items.objects.filter(sales_invoice=salesinvoice_id,deleted=0).aggregate(Sum('discount'))
    salesinvoice=Salesinvoice.objects.get(id=salesinvoice_id)
    if salesinvoice:
        #return_data={"purchaseinvoice_id":purchaseinvoice_id,"otherdata1":bill_amount,"otherdata2":tax_amount,"otherdata3":item_discount}
        #return Response(return_data)
        salesinvoice.bill_amount=bill_amount['bill_amount__sum']
        salesinvoice.tax_amount=tax_amount['tax_amount__sum']
        salesinvoice.net_amount=net_amount['net_amount__sum']
        salesinvoice.item_discount=item_discount['discount__sum']
        salesinvoice.bill_amount_before_tax=bill_amount['bill_amount__sum']-item_discount['discount__sum'];
        salesinvoice.save()

    