from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    
@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'type',
        'name'
    ]
    
@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'name'
    ]
    
@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'name'
    ]
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'name'
    ]
    
@admin.register(models.InputInvoice)
class InputInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'shop',
        'invoice_no'
    ]
    
@admin.register(models.InputData)
class InputDataAdmin(admin.ModelAdmin):
    list_display = [
        'invoice',
        'product'
    ]
