from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    # property
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # contacts
    code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=10, blank=True, null=True)
    fax = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True)
    # address
    province = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    sub_district = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip = models.CharField(max_length=6, blank=True, null=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
