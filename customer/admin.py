from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Customer)
class  CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'contact'
    ]
    
@admin.register(models.Cart)
class  CartAdmin(admin.ModelAdmin):
    list_display = [
        'customer'
    ]
    
@admin.register(models.Order)
class  OrderAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'status',
        'invoice'
    ]