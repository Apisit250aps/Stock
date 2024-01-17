from rest_framework import serializers
from . import models


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = "__all__"

     
class OutputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OutputData
        fields = "__all__"
        
    
class OutputInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OutputInvoice
        fields = "__all__"