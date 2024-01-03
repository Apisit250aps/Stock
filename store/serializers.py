from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class InputInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputInvoice
        fields = "__all__"


class InputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputData
        fields = "__all__"
