from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders

from django.db.models import Sum

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q, F

from datetime import datetime
import json
import random

from . import models
from . import serializers

# Create your views here.


def invoice_code():

    date = datetime.today().date().__str__().replace("-", "")
    if models.InputInvoiceCounter.objects.filter(on_date=date).count() == 0:
        models.InputInvoiceCounter.objects.create(on_date=date)
    else:
        models.InputInvoiceCounter.objects.filter(
            on_date=date).update(no=F('no')+1)
    count = models.InputInvoiceCounter.objects.get(on_date=date)

    return date+"{0:04}".format(int(count.no))


def product_code(category):
    models.ProductCategory.objects.filter(
        id=category).update(count=F('count')+1)
    cats = models.ProductCategory.objects.get(id=category)
    count = "{0:04}".format(cats.count)
    code = f"{cats.id}"+count
    return code


@csrf_exempt
@api_view(["POST", ])
@permission_classes((AllowAny,))
def registerUser(request):
    http_status = status.HTTP_200_OK
    email = request.data['email']
    username = request.data['username']
    password = request.data['password']

    try:
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )
        if user:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_400_BAD_REQUEST

    except:
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response(status=http_status)


@csrf_exempt
@api_view(["POST", ])
@permission_classes((AllowAny,))
def loginUser(request):
    http_status = status.HTTP_200_OK
    username = request.data['username']
    password = request.data['password']

    user = authenticate(
        username=username,
        password=password
    )
    if user is not None:
        if user.is_active:
            http_status = status.HTTP_202_ACCEPTED
            login(request, user)
        else:
            http_status = status.HTTP_406_NOT_ACCEPTABLE
    else:
        http_status = status.HTTP_400_BAD_REQUEST

    return Response(status=http_status)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def getProductType(request):
    product_typeQuery = models.ProductType.objects.all()
    product_typeSerializer = serializers.ProductTypeSerializer(
        product_typeQuery, many=True)
    return Response(status=status.HTTP_200_OK, data=product_typeSerializer.data)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((IsAuthenticated,))
def getProductCategory(request):
    user = User.objects.get(username=request.user.username)
    shop = models.Shop.objects.get(user=user)

    product_CategoryQuery = models.ProductCategory.objects.filter(
        type=int(shop.product_type.id))
    product_CategorySerializer = serializers.ProductCategorySerializer(
        product_CategoryQuery, many=True)
    return Response(status=status.HTTP_200_OK, data=product_CategorySerializer.data)


@csrf_exempt
@api_view(["POST", ])
@permission_classes((IsAuthenticated,))
def createShop(request):
    http_status = status.HTTP_200_OK
    user = request.data['user']
    area = request.data['area']
    product_type = request.data['product_type']
    name = request.data['name']
    contact = request.data['contact']
    tel = request.data['tel']
    fax = request.data['fax']
    email = request.data['email']
    remark = request.data['remark']
    province = request.data['province']
    district = request.data['district']
    sub_district = request.data['sub_district']
    address = request.data['address']

    try:
        shop = models.Shop.objects.create(
            user=user,
            area=area,
            product_type=product_type,
            name=name,
            contact=contact,
            tel=tel,
            fax=fax,
            email=email,
            remark=remark,
            province=province,
            district=district,
            sub_district=sub_district,
            address=address
        )

        if shop:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_400_BAD_REQUEST

    except:
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response(status=http_status)


@csrf_exempt
@api_view(["POST", ])
@permission_classes((IsAuthenticated,))
def updateShop(request):

    return Response()


@csrf_exempt
@api_view(["POST", ])
@permission_classes((AllowAny,))
def createInputData(request):
    user = User.objects.get(username=request.user.username)
    shop = models.Shop.objects.get(user=user)
    total_discount = 0
    total_price = 0
    remark = ""
    invoice_no = invoice_code()

    invoice = models.InputInvoice.objects.create(
        shop=shop,
        invoice_no=invoice_no,
        remark=remark,
    )

    # create product and input data
    products = json.loads(request.data['products'])
    for key, value in products.items():

        total_price += value['total']
        total_discount += value['discount']

        discount = value['discount']
        quantity = value['unit']
        unit_price = value['price']

        del value['total']
        del value['discount']
        value['shop'] = shop
        cats = value['category']
        print(cats, type(cats))

        value['category'] = models.ProductCategory.objects.get(
            id=int(value['category']))
        value['code'] = product_code(cats)

        product = models.Product.objects.create(**value)
        input_data = models.InputData.objects.create(
            product=product,
            quantity=quantity,
            invoice=invoice,
            unit_price=unit_price,
            discount=discount
        )

    models.InputInvoice.objects.filter(id=invoice.id).update(
        total_price=total_price, discount=total_discount)

    return Response(status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def shopInvoice(request):
    user = User.objects.get(username=request.user.username)
    shop = models.Shop.objects.get(user=user)

    invoiceQuery = models.InputInvoice.objects.filter(
        shop=shop).order_by('-updated_at')
    invoiceSerializer = serializers.InputInvoiceSerializer(
        invoiceQuery, many=True)

    return Response(status=status.HTTP_200_OK, data=invoiceSerializer.data)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((IsAuthenticated,))
def ShopProducts(request):
    http_status = status.HTTP_200_OK

    user = User.objects.get(username=request.user.username)
    shop = models.Shop.objects.get(user=user)

    productQuery = models.Product.objects.filter(shop=shop).order_by('-updated_at')
    productSerializers = serializers.ProductSerializer(productQuery, many=True)

    return Response(status=http_status, data=productSerializers.data)
