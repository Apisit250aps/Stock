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

