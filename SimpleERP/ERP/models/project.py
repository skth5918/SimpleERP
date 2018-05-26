from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.exceptions import NON_FIELD_ERRORS


class project(models.Model):
    project_name = models.CharField(max_length=100)
    project_est_amt = models.FloatField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True, default=None)
    project_net_amt = models.FloatField(max_length=100, default=None)
    status = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='project_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='project_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("project_name", "deleted"),
        ]

class project_item(models.Model):
    item_name = models.CharField(max_length=100)
    project = models.ForeignKey(
        project, on_delete=models.CASCADE, blank=True, null=True)
    project_type = models.CharField(max_length=100)
    quantity = models.FloatField(max_length=100,default=0)
    rate = models.FloatField(max_length=100,default=0)
    amount = models.FloatField(max_length=100,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='project_item_Created_By_User', default=1)
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='project_item_Modified_By_User', default=1)
    deleted = models.BooleanField(default=False)