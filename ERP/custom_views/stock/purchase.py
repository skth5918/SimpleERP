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
from .stockentry import *
from django.db import connection
from django.db.models import Sum



row_per_page = settings.GLOBAL_SETTINGS['row_per_page']


@api_view(['GET', 'POST'])
def purchase_items_create(request):
    if request.method == 'GET':
        return Response({'data':'', 'module':'Purchase'}, template_name='ERP/stock/purchase/create_update.html')
    else:
        mutable = request.POST._mutable
        request.POST._mutable = True
        error_details = []
        if not request.POST["purchaseinvoice_id"]:
            company_id=session_user_company(request);
            if request.POST['bill_mode']==1:
                mode="PI"
            else:
                mode="PINT"
            series=serires_values(company_id,mode)
            entry_date=db_store_date(request.POST['entry_date'])
            data={
                "series":series,
                "entry_date":entry_date,
                "warehouse":request.POST['warehouse'],
                "supplier":request.POST['supplier'],
                "supplier_bill_no":request.POST['supplier_bill_no'],
                "description":request.POST['description'],
                "bill_mode":request.POST['bill_mode'],
                }
            serializer = PurchaseInvoiceSerializer(data=data)
            serializer.is_valid()
            if serializer.is_valid():
                user_id= session_user_id(request)
                date_modified=store_date_time()
                purchaseinvoice=serializer.save(created_by=user_id,created_date=date_modified)
                purchaseinvoice_id=purchaseinvoice.id
                
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
        else:
            purchaseinvoice_id=request.POST["purchaseinvoice_id"]
        if purchaseinvoice_id:
            if not request.POST['discount']:
                discount=0
            else:
                discount=request.POST['discount'];
            bill_amount_before_tax=float(request.POST['bill_amount'])-float(discount)
            data_purchaseinvoice_items={
                "purchaseinvoice":purchaseinvoice_id,
                "item":request.POST['item'],
                "qty":request.POST['qty'],
                "rate":request.POST['rate'], 
                "bill_amount":request.POST['bill_amount'],
                "discount":discount,
                "bill_amount_before_tax":bill_amount_before_tax,
                "tax_per":request.POST['tax_per'],
                "tax_amount":request.POST['tax_amount'],
                "net_amount":request.POST['net_amount'],
                "batchno":request.POST['batchno'],
                "taxgroup" :request.POST['taxgroup_id'],
                "warehouse":request.POST['warehouse'],
                'deleted':0
                

                }
            serializer = PurchaseInvoice_ItemsSerializer(data=data_purchaseinvoice_items)
            serializer.is_valid()
            if serializer.is_valid():
                user_id= session_user_id(request)
                date_modified=store_date_time()
                company_id=session_user_company(request);
                purcahseinvoice_items=serializer.save(company=company_id,created_by=user_id,created_date=date_modified)
                purchase_invoice_items_id=purcahseinvoice_items.id
                item_id=request.POST['item']
                item_details=Item.objects.get(pk=item_id)
                invoice_rate_update(purchaseinvoice_id)
                if item_details.serial:
                    serial_nos=request.POST['serial_nos']
                    serial_nos=serial_nos.strip("")
                    if serial_nos:
                        #pass
                        
                        val=Serial_no_create(2,purchase_invoice_items_id,serial_nos,2,request)
                    else:
                        #pass
                        val=Serial_no_create(2,purchase_invoice_items_id,None,1,request)
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
                
        return_data={"purchaseinvoice_id":purchaseinvoice_id,"error_details":error_details}
        return Response(return_data)
    
    

@api_view(['GET'])
def purchase_items(request):
    html=None
    model_obj=[]
    #return Response("Hai")
    if request.is_ajax() and request.GET['id']:
        id=request.GET['id']
        data = []
        #return Response(request.GET['id'])
        custom_filter={}
        custom_filter['deleted']=0
        custom_filter['purchaseinvoice_id']=id
        
        model_obj = PurchaseInvoice_Items.objects.filter(**custom_filter)
        model_obj_invoice = PurchaseInvoice.objects.get(pk=id)
            
        #data = Stockentry_itemsSerializer(model_obj, many=True).data
    html = render_to_string('ERP/stock/purchase/purchase_items.html', {'data': model_obj,"basic_data":model_obj_invoice})
    #html = render_to_string('ERP/stock/test.html', {'data': request})
    return HttpResponse(html)

@api_view(['GET'])
def purchaseitems_delete(request):
    if request.is_ajax() and request.GET['id']:
        id=request.GET['id']
        selected_values=PurchaseInvoice_Items.objects.get(pk=request.GET['id'])
        user_id= session_user_id(request)
        date_modified=store_date_time()
        selected_values.modified_date=date_modified
        selected_values.modified_by=user_id
        selected_values.deleted=1
        selected_values.save();
        invoice_rate_update(selected_values.purchaseinvoice_id)
        with connection.cursor() as cursor:
            query_serial_no_tracking="update ERP_serial_no_tracking set deleted=1 where ref_type=2 and ref_id=%s" %(id)
            cursor.execute(query_serial_no_tracking)
         
            query_serial_no="""update ERP_serial_no set deleted=1 where id in (select serial_no_id_id from ERP_serial_no_tracking where  ref_type=2 
            and ref_id=%s)""" %(id) 
            cursor.execute(query_serial_no)
    return HttpResponse("1")

@api_view(['GET', 'POST'])
def purchase_create(request):
    data=[]
    if request.method == 'GET':
        return Response({'data':'', 'module':'Purchase Invoice'}, template_name='ERP/stock/purchase/create_update.html')
    else:
        if request.POST['purchaseinvoice_id']:
            purchaseinvoice_id=request.POST['purchaseinvoice_id']
            purchase_submit_confirm(purchaseinvoice_id,request)
    if request.accepted_renderer.format == 'html':
                return Response({"error_data": data}, template_name='ERP/stock/purchase/create_update.html')
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def serial_nos(request):
    from io import BytesIO
    from reportlab.pdfgen import canvas 
    from weasyprint import HTML
    from django.core.files.storage import FileSystemStorage
    # Create the HttpResponse object with the appropriate PDF headers.
    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    html_string = render_to_string('ERP/stock/pdf.html', {'paragraphs': paragraphs})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response
        
@api_view(['GET', 'POST'])
def purchase_update(request, id):
    data=[]
    if request.method == 'GET':
        data=PurchaseInvoice.objects.get(pk=id)
        return Response({'data':data, 'module':'Purchase Invoice'}, template_name='ERP/stock/purchase/create_update.html')
    else:
        if request.POST['purchaseinvoice_id']:
            purchaseinvoice_id=request.POST['purchaseinvoice_id']
            purchase_submit_confirm(purchaseinvoice_id,request)
    if request.accepted_renderer.format == 'html':
        return Response({"error_data": data}, template_name='ERP/stock/purchase/create_update.html')
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

def purchase_submit_confirm(purchaseinvoice_id,request):
    purchase=PurchaseInvoice.objects.get(id=purchaseinvoice_id)
    
    if purchase:
        invoice_discount=request.POST['invoice_discount'];
        if float(invoice_discount)>0:
            #return Response({'data':request.POST['new_net_amount'], 'module':'Purchase'}, template_name='ERP/stock/test.html')
            purchase.discount=float(request.POST['invoice_discount'])
            purchase.net_amount=float(request.POST['new_net_amount'])
            purchase.tax_amount=float(request.POST['new_tax_amount']);
        purchase.status=1
        purchase.save()
        bill_amount_before_tax=purchase.bill_amount_before_tax;
        purchaseitem_list=PurchaseInvoice_Items.objects.all().filter(purchaseinvoice=purchaseinvoice_id,deleted=0)
        for purchaseitem_list_val in purchaseitem_list:
            ref_type=1
            ref_id=purchaseitem_list_val.id
            qty=purchaseitem_list_val.qty
            item=purchaseitem_list_val.item
            warehouse=purchaseitem_list_val.warehouse
            company=purchaseitem_list_val.company
            bill_amount=purchaseitem_list_val.bill_amount
            discount=purchaseitem_list_val.discount
            tax_per=purchaseitem_list_val.tax_per
            tax_amount=purchaseitem_list_val.tax_amount
            if float(invoice_discount)>0:
                purchaseinvoice_items=PurchaseInvoice_Items.objects.get(id=ref_id)
                item_bill_amount_before_tax=purchaseitem_list_val.bill_amount_before_tax
                new_discount=float(invoice_discount)/float(bill_amount_before_tax)*float(item_bill_amount_before_tax)
                new_disccount_plus_old=new_discount+discount
                new_bill_amount_before_tax=bill_amount-new_disccount_plus_old
                new_tax=tax_amount;
                if float(tax_amount)>0:
                    new_tax=float(new_bill_amount_before_tax)*float(tax_per)/float(100)
                purchaseinvoice_items.discount=new_disccount_plus_old
                purchaseinvoice_items.bill_amount_before_tax=new_bill_amount_before_tax
                purchaseinvoice_items.net_amount=new_bill_amount_before_tax+new_tax
                purchaseinvoice_items.tax_amount=new_tax
                purchaseinvoice_items.save();
                
                
                
            
            ref_name="Purchase Create"
            mode=1
            data=stock_create_update(item, qty, warehouse, company, mode, ref_id, 2, ref_name,request)
        #return HttpResponse(data)
            

    #return Response({"data": "Stockentry Updated successfully"}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def purchase_list(request):
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
    model_obj = PurchaseInvoice.objects.filter(**custom_filter)
    model_data = PurchaseInvoiceSerializer(model_obj, many=True).data
    page = request.GET.get('page', 1)
    paginator = Paginator(model_data, row_per_page)
    try:
        model_data = paginator.page(page)
    except PageNotAnInteger:
        model_data = paginator.page(1)
    except EmptyPage:
        model_data = paginator.page(paginator.num_pages)
    if request.accepted_renderer.format == 'html':
        return Response({"data": model_data,'module':'Purchase Invoice',"custom_filter":custom_filter}, template_name='ERP/stock/purchase/list.html')
    return Response({"data": model_data,"custom_filter":custom_filter}, status=status.HTTP_200_OK)




def invoice_rate_update(purchaseinvoice_id):
    # Rate Updatation
    bill_amount = PurchaseInvoice_Items.objects.filter(purchaseinvoice=purchaseinvoice_id,deleted=0).aggregate(Sum('bill_amount'))
    tax_amount = PurchaseInvoice_Items.objects.filter(purchaseinvoice=purchaseinvoice_id,deleted=0).aggregate(Sum('tax_amount'))
    net_amount = PurchaseInvoice_Items.objects.filter(purchaseinvoice=purchaseinvoice_id,deleted=0).aggregate(Sum('net_amount'))
    item_discount = PurchaseInvoice_Items.objects.filter(purchaseinvoice=purchaseinvoice_id,deleted=0).aggregate(Sum('discount'))
    purchaseinvoice=PurchaseInvoice.objects.get(id=purchaseinvoice_id)
    if purchaseinvoice:
        #return_data={"purchaseinvoice_id":purchaseinvoice_id,"otherdata1":bill_amount,"otherdata2":tax_amount,"otherdata3":item_discount}
        #return Response(return_data)
        purchaseinvoice.bill_amount=bill_amount['bill_amount__sum']
        purchaseinvoice.tax_amount=tax_amount['tax_amount__sum']
        purchaseinvoice.net_amount=net_amount['net_amount__sum']
        purchaseinvoice.item_discount=item_discount['discount__sum']
        purchaseinvoice.bill_amount_before_tax=bill_amount['bill_amount__sum']-item_discount['discount__sum'];
        purchaseinvoice.save()
                    

@api_view(['GET', 'POST','Delete'])
#@permission_classes((IsAuthenticated, ))
def purchase_view(request, id):
    #return Response({'data':id}, template_name='ERP/stock/test.html')
    if request.method == 'GET':
        try:
            id=int(id)
            data=PurchaseInvoice.objects.get(pk=id)
            return Response({'data':data, 'module':'Purchase Invoice'}, template_name='ERP/stock/purchase/create_update.html')
        except:
             return Response({'data':'', 'module':'Purchase Invoice'}, template_name='ERP/stock/purchase/create_update.html')
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