from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.exceptions import NON_FIELD_ERRORS


# Create your models here.
class Currency(models.Model):
    """Details of Currency Entity"""
    name = models.CharField(max_length=50, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Currency_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Currency_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "country","deleted"),
        ]
class StateMaster(models.Model):
    """docstring for StateMaster"""
    state = models.CharField(max_length=50, null=False, blank=False)
    state_code = models.CharField(max_length=50, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='StateMaster_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='StateMaster_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("state", "state_code","deleted"),
        ]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Company(models.Model):
    """Details of Company Entity"""
    name = models.CharField(max_length=50, blank=False, null=False)
    short_name = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=13)
    email = models.EmailField(max_length=50)
    address = models.TextField(max_length=300, blank=False, null=False)
    gst_no = models.CharField(max_length=30 ,null=True)
    cst_no = models.CharField(max_length=30, null=True)
    tin_no = models.CharField(max_length=30 ,null=True)
    pan_no = models.CharField(max_length=10 ,null=True)
    bank_name = models.TextField(max_length=50, blank=False, null=False)
    account_holder_name = models.TextField(
        max_length=50, blank=False, null=False)
    account_no = models.CharField(blank=True, null=True,max_length=25)
    ifsc_code = models.TextField(max_length=30, blank=True, null=True)
    default_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name='Company_Currency')
    state= models.ForeignKey(
        StateMaster, on_delete=models.CASCADE, related_name='Company_State')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Company_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Company_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "short_name","deleted"),
        ]

class WareHouse(models.Model):
    """docstring for WareHouse"""
    warehouse_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_default = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='WareHouse_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='WareHouse_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("warehouse_name", "company","deleted"),
        ]
class Unit(models.Model):
    """docstring for Field"""
    unit_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Field_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Field_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    error_messages={}
    class Meta:
        unique_together = [
            ("unit_name", "deleted"),
        ]
        
class ItemGroup(models.Model):
    """docstring for itemgroup"""
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ItemGroup_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ItemGroup_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "deleted"),
        ]
    
class CustomerGroup(models.Model):
    """docstring for CustomerGroup"""
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='CustomerGroup_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='CustomerGroup_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "deleted"),
        ]

class Customer(models.Model):
    """docstring for Customer"""
    name = models.CharField(max_length=100)
    customergroup = models.ForeignKey(CustomerGroup, on_delete=models.CASCADE)
    primary_contact_no = models.CharField(max_length=50)
    email_id = models.EmailField()
    contact_person = models.CharField(max_length=50,blank=True, null=True)
    contact_person_contact_no = models.CharField(max_length=50,blank=True, null=True)
    contact_person_email_id = models.EmailField(max_length=50,blank=True, null=True)
    secondary_contact_no = models.CharField(max_length=50,blank=True, null=True)
    secondary_email_id = models.EmailField(blank=True, null=True)
    referred_by = models.IntegerField(default=False)
    address = models.CharField(max_length=200)
    #state = models.CharField(max_length=50)
    state= models.ForeignKey(StateMaster, on_delete=models.CASCADE, related_name='customer_State')
    max_credit_amount = models.IntegerField()
    credit_days = models.IntegerField()
    credit_status = models.CharField(max_length=30)
    billing_address = models.CharField(max_length=200)
    shiping_address = models.CharField(max_length=200)
    gst_no = models.CharField(max_length=20,blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Customer_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Customer_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)

class TaxGroup(models.Model):
    """docstring for TaxGroup"""
    name = models.CharField(max_length=100)
    tax_per = models.FloatField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='TaxGroup_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='TaxGroup_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "deleted"),
        ]
class Tax(models.Model):
    """docstring for Tax"""
   
    tax_group = models.ForeignKey(TaxGroup, on_delete=models.CASCADE)
    tax_name = models.CharField(max_length=100)
    tax_per = models.FloatField(max_length=20)
    tax_type=models.IntegerField(default=1)
    #buying = models.BooleanField(default=False)
    #selling = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Tax_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Tax_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("tax_group","tax_name", "deleted"),
        ]
class SupplierGroup(models.Model):
    """docstring for CustomerGroup"""
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='SupplierGroup_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='SupplierGroup_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "deleted"),
        ]

class Supplier(models.Model):
    """docstring for Supplier"""
    name = models.CharField(max_length=100)
    suppliergroup = models.ForeignKey(SupplierGroup, on_delete=models.CASCADE)
    primary_contact_no = models.CharField(max_length=100,blank=True, null=True)
    email_id = models.EmailField()
    contact_person = models.CharField(max_length=100,blank=True, null=True)
    contact_person_contact_no = models.CharField(max_length=50,blank=True, null=True)
    contact_person_email_id = models.CharField(max_length=20,blank=True, null=True)
    secondary_contact_no = models.CharField(max_length=20,blank=True, null=True)
    secondary_email_id = models.CharField(max_length=20,blank=True, null=True)
    address = models.CharField(max_length=200)
    state= models.ForeignKey(
        StateMaster, on_delete=models.CASCADE, related_name='Supplier_State')
    gst_no = models.CharField(max_length=20,blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank_name = models.TextField(max_length=50, blank=True, null=True)
    account_holder_name = models.TextField(
        max_length=50, blank=True, null=True)
    account_no = models.CharField(max_length=50,blank=True, null=True)
    ifsc_code = models.TextField(max_length=30, blank=True, null=True)
    default_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name='Supplier_Currency')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Supplier_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Supplier_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    unique_together = [
            ("name", "primary_contact_no","deleted","company"),
        ]
class ItemColor(models.Model):
    """docstring for TaxGroup"""
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ItemColor_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ItemColor_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "deleted"),
        ]
class ItemSize(models.Model):
    """docstring for TaxGroup"""
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ItemSize_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ItemSize_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "deleted"),
        ]
class ItemBrand(models.Model):
    """docstring for TaxGroup"""
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ItemBrand_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ItemBrand_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("name", "deleted"),
        ]




class Item(models.Model):
    """docstring for TaxGroup"""
    name = models.CharField(max_length=250)
    item_code = models.CharField(max_length=250)
    hsn_code = models.CharField(max_length=250,blank=True, null=True)
    color = models.ForeignKey(
        ItemColor, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(
        ItemSize, on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(
        ItemBrand, on_delete=models.CASCADE, blank=True, null=True)

    group = models.ForeignKey(
        ItemGroup, on_delete=models.CASCADE, blank=True, null=True)
    variants = models.BooleanField(default=False)
    variants_of=models.IntegerField(default=0)
    purchase_unit = models.ForeignKey(Unit, on_delete=models.CASCADE,related_name='Item_Purchase_Unit', blank=True, null=True)

    sales_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,related_name='Item_Sales_Unit', blank=True, null=True)

    serial=models.BooleanField(default=False)
    batch=models.BooleanField(default=False)
    serial_prefix=models.CharField(max_length=10,blank=True, null=True)
    convertion_qty = models.FloatField(max_length=20,default=1)
    maintain_stock=models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Item_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Item_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    tax_group = models.ForeignKey(TaxGroup, on_delete=models.CASCADE)
    serial_no_count=models.IntegerField(default=0)
    class Meta:
        unique_together = [
            ("name","item_code", "deleted"),
        ]

class Series(models.Model):
    
    series_prefix=models.CharField(max_length=100)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,default=1)
    series_count=models.IntegerField(default=0)
    series_for=models.CharField(max_length=50)
    is_default=models.BooleanField(default=True)
    
    
    
    
    