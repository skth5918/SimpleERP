from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.exceptions import NON_FIELD_ERRORS
from .masters import *





class expensecategory(models.Model):
    category_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expensecategory_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expensecategory_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("category_name", "deleted"),
        ]

class expense(models.Model):
    expense_amt = models.FloatField(default=0)
    expense_category = models.ForeignKey(
        expensecategory, on_delete=models.CASCADE, blank=True, null=True)
    bill = models.BooleanField(default=False)
    description = models.TextField(default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expense_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expense_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    bill_no = models.IntegerField(default=None)
    supplier = models.CharField(max_length=100, default=None)
    tax = models.FloatField(max_length=100,default=0)
    net_total = models.FloatField(max_length=100,default=0)
