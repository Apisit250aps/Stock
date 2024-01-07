from django.db import models
from django.contrib.auth.models import User

import random as rd 
# Create your models here.

INVOICE_TYPE = (
    (1, "new"),
    (2, "add")
)
class ProductType(models.Model):
    # property
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=0, blank=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return self.name
    
class ProductCategory(models.Model):
    # property
    id = models.BigAutoField(primary_key=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=0, blank=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return self.name
    
class Area(models.Model):
    # property
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=2, unique=True, blank=True)
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=0, blank=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Shop(models.Model):
    # property
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    # information
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=10, blank=True)
    fax = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    remark = models.TextField(blank=True)
    # address
    province = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)
    sub_district = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True, null=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    # property
    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    # information
    code = models.CharField(max_length=8, unique=True, null=True)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    unit = models.IntegerField()
    cost = models.DecimalField(max_digits=9, decimal_places=2)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class ProductDelete(models.Model):
    # property
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.IntegerField()
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product
    
class InputInvoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=16, unique=True, null=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    type=models.IntegerField(choices=INVOICE_TYPE, default=1)
    remark = models.TextField(blank=True, null=True)
    # timestamp 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.invoice_no

class InputData(models.Model):
    id = models.BigAutoField(primary_key=True)
    invoice = models.ForeignKey(InputInvoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=9, decimal_places=2)
    # timestamp 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name
    
class InputInvoiceCounter(models.Model):
    on_date = models.CharField(max_length=8)
    no = models.IntegerField(default=1)