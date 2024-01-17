from django.db import models
from django.contrib.auth.models import User

from store.models import (
    Shop,
    Product,
)
# Create your models here.

ORDER_STATUS = (
    (1, "Pending"),
    (2, "Processing"),
    (3, "Completed"),
    (4, "Shipped"),
    (6, "Cancelled"),
    (5, "Failed"),
    (7, "Delivered"),
    (8, "Refunded"),
)


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


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.IntegerField()

    def __str__(self):
        return self.product


class OutputInvoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=16, unique=True, null=True)
    discount = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, default=0)
    remark = models.TextField(blank=True, null=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_no


class OutputData(models.Model):
    id = models.BigAutoField(primary_key=True)
    invoice = models.ForeignKey(OutputInvoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=9, decimal_places=2)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    order_code = models.CharField(max_length=12)
    order_status = models.IntegerField(choices=ORDER_STATUS)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.IntegerField()

    def __str__(self):
        return self.order.order_code
    
