from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ERP.models import *
from ERP.serializers.serializers import *

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = project.objects.all()

class ProjectItemViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectItemSerializer
    queryset = project_item.objects.all()

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = expense.objects.all()

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    """docstring for ItemGroupViewSet"""
    serializer_class = ExpenseCategorySerializer
    queryset = expensecategory.objects.all()

class ProfileViewSet(viewsets.ModelViewSet):
    """docstring for UserViewSet"""
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


class CurrencyViewSet(viewsets.ModelViewSet):
    """docstring for CurrencyViewSet"""
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    """docstring for CompanyViewSet"""
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class WareHouseViewSet(viewsets.ModelViewSet):
    """docstring for WareHouseViewSet"""
    serializer_class = WareHouseSerializer
    queryset = WareHouse.objects.all()


class FieldViewSet(viewsets.ModelViewSet):
    """docstring for FieldViewSet"""
    serializer_class = FieldSerializer
    queryset = Field.objects.all()


class ItemGroupViewSet(viewsets.ModelViewSet):
    """docstring for ItemGroupViewSet"""
    serializer_class = ItemGroupSerializer
    queryset = ItemGroup.objects.all()


class CustomerGroupViewSet(viewsets.ModelViewSet):
    """docstring for CustomerGroupViewSet"""
    serializer_class = CustomerGroupSerializer
    queryset = CustomerGroup.objects.all()


class CustomerViewSet(viewsets.ModelViewSet):
    """docstring for CustomerViewSet"""
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class TaxGroupViewSet(viewsets.ModelViewSet):
    """docstring for TaxGroupViewSet"""
    serializer_class = TaxGroupSerializer
    queryset = TaxGroup.objects.all()


class TaxViewSet(viewsets.ModelViewSet):
    """docstring for TaxViewSet"""
    serializer_class = TaxSerializer
    queryset = Tax.objects.all()


class SupplierViewSet(viewsets.ModelViewSet):
    """docstring for SupplierViewSet"""
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
