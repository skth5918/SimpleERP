from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.exceptions import NON_FIELD_ERRORS
from .masters import *
#from ERP.masters import  *

class Price(models.Model):
    """docstring for StateMaster"""
    item=models.ForeignKey(
        Item, on_delete=models.CASCADE, blank=False, null=False)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=1)
    max_discount_per=models.FloatField(default=0)
    buying_price=models.FloatField(default=0)
    buying_tax_group=models.ForeignKey(TaxGroup,on_delete=models.CASCADE,default=None,related_name="Price_buying_tax_group")
    buying_tax_amount=models.FloatField(default=0)
    buying_price_with_tax=models.FloatField(default=0)
    selling_price=models.FloatField(default=0)
    selling_tax_group=models.ForeignKey(TaxGroup,on_delete=models.CASCADE,default=None,related_name="Price_selling_tax_group")
    selling_tax_amount=models.FloatField(default=0)
    selling_price_with_tax=models.FloatField(default=0)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,default=1,related_name="Price_Created_By_User")
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE,default=1,related_name="Price_Modified_By_User")
    deleted = models.BooleanField(default=False)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=1)
    
    class Meta:
        unique_together = [
            ("item", "company","deleted"),
        ]
class Pricelog(models.Model):
    """docstring for StateMaster"""
    item=models.ForeignKey(
        Item, on_delete=models.CASCADE, blank=False, null=False)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=1)
    selling_price=models.FloatField(default=0)
    selling_tax_group=models.ForeignKey(TaxGroup,on_delete=models.CASCADE,default=None,related_name="PriceLog_selling_tax_group")
    selling_tax_amount=models.FloatField(default=0)
    selling_price_with_tax=models.FloatField(default=0)
    max_discount_per=models.FloatField(default=0)
    buying_price=models.FloatField(default=0)
    buying_tax_group=models.ForeignKey(TaxGroup,on_delete=models.CASCADE,default=None,related_name="PriceLog_buying_tax_group")
    buying_tax_amount=models.FloatField(default=0)
    buying_price_with_tax=models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,default=1,related_name="PriceLog_Created_By_User")
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE,default=1,related_name="PriceLog_Modified_By_User")
    deleted = models.BooleanField(default=False)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=1)
    
class Salesinvoice(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=1)
    sales_date = models.DateTimeField()
    customer=models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    series=models.CharField(max_length=100,default=None)
    bill_mode=models.IntegerField(default=0)
    bill_type=models.IntegerField(default=0)
    bill_amount=models.FloatField(default=0)
    item_discount=models.FloatField(default=0)
    discount=models.FloatField(default=0)
    bill_amount_before_tax=models.FloatField(default=0)
    tax_amount=models.FloatField(default=0)
    net_amount=models.FloatField(default=0)
    paid_amount=models.FloatField(default=0)
    balance_amount=models.FloatField(default=0)
    credit_date=models.DateField(blank=True, null=True)
    status=models.IntegerField(default=0) # 0- Draft,1-Submitted,2-Canceled
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,default=1,related_name="sales_Created_By_User")
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE,default=1,related_name="aales_Modified_By_User")
    deleted = models.BooleanField(default=False)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=1)


class SalesInvoice_Items(models.Model):
    sales_invoice=models.ForeignKey(
    Salesinvoice, on_delete=models.CASCADE, blank=False, null=False)
    item=models.ForeignKey(
        Item, on_delete=models.CASCADE, blank=False, null=False)
    warehouse=models.ForeignKey(
        WareHouse, on_delete=models.CASCADE, blank=True, null=True)
    qty=models.FloatField(default=0)
    rate=models.FloatField(default=0)
    taxgroup=models.ForeignKey(
        TaxGroup, on_delete=models.CASCADE, blank=True, null=True)
    bill_amount=models.FloatField(default=0)
    discount=models.FloatField(default=0)
    tax_per=models.FloatField(default=0)
    bill_amount_before_tax=models.FloatField(default=0)
    tax_amount=models.FloatField(default=0)
    net_amount=models.FloatField(default=0)
    batchno=models.CharField(max_length=100,default=None,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,  default=1,related_name="salesInvoice_items_Created_By_User")
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE,  default=1,related_name="salesInvoice_items_Modified_By_User")
    deleted = models.BooleanField(default=False)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=1)
    