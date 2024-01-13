from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductType
        fields = "__all__"

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = "__all__"

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = "__all__"

class InputInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputInvoice
        fields = "__all__"


class InputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputData
        fields = "__all__"

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = "__all__"