# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-18 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0024_auto_20180516_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesinvoice_items',
            name='discount_per',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='salesinvoice_items',
            name='discount_val',
            field=models.FloatField(default=0),
        ),
    ]
