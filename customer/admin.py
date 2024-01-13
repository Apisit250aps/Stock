from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Customer)
class  CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'contact'
    ]