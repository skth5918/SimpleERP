# Generated by Django 2.0 on 2018-04-13 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxgroup',
            old_name='tax_per',
            new_name='tax_max_per',
        ),
    ]