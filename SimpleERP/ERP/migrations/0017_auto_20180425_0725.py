# Generated by Django 2.0 on 2018-04-25 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0016_auto_20180424_0547'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='purpose',
            new_name='bill_mode',
        ),
    ]