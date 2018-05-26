# Generated by Django 2.0 on 2018-04-22 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ERP', '0011_stockentry_series'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price', models.FloatField(default=0)),
                ('selling_price_with_tax', models.FloatField(default=0)),
                ('max_discount_per', models.FloatField(default=0)),
                ('buying_price', models.FloatField(default=0)),
                ('buying_price_with_tax', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ERP.Company')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Price_Created_By_User', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.Item')),
                ('modified_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Price_Modified_By_User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pricelog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price', models.FloatField(default=0)),
                ('selling_price_with_tax', models.FloatField(default=0)),
                ('max_discount_per', models.FloatField(default=0)),
                ('buying_price', models.FloatField(default=0)),
                ('buying_price_with_tax', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ERP.Company')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='PriceLog_Created_By_User', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.Item')),
                ('modified_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='PriceLog_Modified_By_User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together={('item', 'company', 'deleted')},
        ),
    ]