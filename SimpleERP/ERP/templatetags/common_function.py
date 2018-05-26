from datetime import datetime
from django import template
from random import choice
register = template.Library()
from ERP.models.masters import *
from django.db import connection



purpose = {1: 'Stock Receipt', 2: 'Stock Transfer',3:'Stock Scrap'}
series_choices = (
        ('SE', 'Stock Entry'),
        ("PI", 'Purchase Invice'),
        ('SI', 'Sales Invoice'),
        ('SEI', 'Service Invoice'),
        ('EX', 'Expense'),
        ('SO', 'Sales Order'),
        ('PO', 'Sales Order'),
        ('QU', 'Quotation'),
        )

stock_entry_status_dic={"0":"Draft","1":"Submitted"}

@register.simple_tag
def current_year():
	#return "Something"
    return datetime.now().strftime("%Y")

@register.simple_tag
def current_date():
    #return "Something"
    return datetime.today().strftime("%d-%m-%Y")


@register.simple_tag
def default_customer_id():
    default_customer=Customer.objects.get(default_cash_customer=1,deleted=0)
    return default_customer.id
             
@register.simple_tag
def default_customer_name():
    default_customer=Customer.objects.get(default_cash_customer=1,deleted=0)
    return default_customer.name

@register.simple_tag
def stock_entry_status(status):
    #global stock_entry_status_dic
    return stock_entry_status_dic[str(status)]

@register.simple_tag
def stock_entry_delete(stock_entry_id):
    pass
    #return datetime.now().strftime("%Y")


@register.simple_tag
def application_name():
	return " ERP"



@register.simple_tag
def show_single_field(tableName,show_field_name,pk):
    data = []
    with connection.cursor() as cursor:
        if tableName and pk and show_field_name:
            query = "SELECT  `%s` FROM %s where id=%s" %(show_field_name,tableName,pk)
            #return query
            cursor.execute(query)
            row = cursor.fetchone()
            return row[0]

@register.simple_tag
def show_single_row(tableName,show_field_name,pk):
    data = []
    with connection.cursor() as cursor:
        query = "SELECT  `%s` FROM %s where id=%s" %(show_field_name,tableName,pk)
        #return query
        cursor.execute(query)
        row = cursor.fetchone()
        return row[0]

@register.simple_tag
def show_row_list(tableName,ref_name,ref_id):
    data = []
    with connection.cursor() as cursor:
        query = "SELECT  * FROM %s where `%s`=%s" %(tableName,ref_name,ref_id)
        #return query
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

@register.simple_tag
def show_serial_nos(id,type):
    data = ""
    #return "hai"
    with connection.cursor() as cursor:
        query = "SELECT  ser.serial_no as serial_no FROM ERP_serial_no ser,ERP_serial_no_tracking tra where tra.ref_id=%s and tra.ref_type=%s and ser.id=tra.serial_no_id_id" %(id,type)
        #return query
        cursor.execute(query)
        rows = cursor.fetchall()
        for obj in rows:
            data+=str(obj[0])+"\n"
        return data
       

@register.simple_tag
def drop_down_list(tableName,show_field_name,store_field_name):
	data = []
	with connection.cursor() as cursor:
		query = "SELECT %s, %s FROM %s where deleted='0'" %(store_field_name,show_field_name,tableName)
		#return query
		cursor.execute(query)
		rows = cursor.fetchall()
		for obj in rows:
			data.append({"id":(obj[0]),"text":(obj[1])})
		return data

@register.simple_tag
def drop_down_choice(choice_name):
	data = []
	if choice_name=="purpose":
		dict_name=purpose
	for k, v in dict_name.items():
		#print k, v
		data.append({"id":k,"text":v})
	return data
	
	
	