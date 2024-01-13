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
from datetime import timedelta
import json
import random

from . import models
from customer import models as customer_models
from .models import (
    INVOICE_TYPE,
)
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


def product_code(category, shop):
    models.ProductCategory.objects.filter(
        id=category).update(count=F('count')+1)
    cats = models.ProductCategory.objects.get(id=category)
    count = "{0:04}".format(cats.count)
    code = f"{shop.id}{cats.id}"+count

    return code


def choiceMap(choice, map):
    for i in choice:
        if i[0] == map:
            return i[1]


def inputInvoiceData(invoiceSerializer):
    InvoiceData = []

    for inv in invoiceSerializer.data:
        invoice = int(inv['id'])
        inv['shop'] = serializers.ShopSerializer(models.Shop.objects.get(id=int(inv['shop']))).data

        inv['type'] = choiceMap(INVOICE_TYPE, inv['type'])

        inputDataQuery = models.InputData.objects.filter(invoice=invoice)
        inputDataSerializer = serializers.InputDataSerializer(
            inputDataQuery, many=True)

        inputDataData = []
        for inp in inputDataSerializer.data:
            product = int(inp['product'])
            productQuery = models.Product.objects.get(id=product)
            productSerializer = serializers.ProductSerializer(productQuery)
            inp['product'] = productSerializer.data
            cats = inp['product']['category']
            inp['product']['category'] = models.ProductCategory.objects.get(
                id=cats).name
            inp['product']['shop'] = inv['shop']
            inputDataData.append(inp)
        inv['input_data'] = inputDataData

        InvoiceData.append(inv)

    return InvoiceData

def cusCode():
    code = "{0:06}".format(random.randint(0, 99999))
    print(code)
    if customer_models.Customer.objects.filter(code=code).count() != 0:
        cusCode()
    
    return code

def shopCode():
    code = "{0:06}".format(random.randint(0, 99999))
    print(code)
    if models.Shop.objects.filter(code=code).count() != 0:
        shopCode()
    
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
            code = cusCode()
            customer_models.Customer.objects.create(user=user, code=code)
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_400_BAD_REQUEST

    except IOError as err:
        print(err)
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
@api_view(["GET", ])
@permission_classes((AllowAny,))
def getArea(request):
    
    return Response(
        serializers.AreaSerializer(models.Area.objects.all(), many=True).data
    )


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def shopData(request):
    user = User.objects.get(username=request.user.username)
    http_status = status.HTTP_200_OK
    try :
        models.Shop.objects.get(user=user)
    
    except:
        http_status = status.HTTP_204_NO_CONTENT
    
    
    return Response(status=http_status)


@csrf_exempt
@api_view(["POST", ])
@permission_classes((IsAuthenticated,))
def createShop(request):
    http_status = status.HTTP_200_OK
    user = User.objects.get(username=request.user.username)
    # user = request.data['user']
    # area = request.data['area']
    # product_type = request.data['product_type']
    # name = request.data['name']
    # contact = request.data['contact']
    # tel = request.data['tel']
    # fax = request.data['fax']
    # email = request.data['email']
    # remark = request.data['remark']
    # province = request.data['province']
    # district = request.data['district']
    # sub_district = request.data['sub_district']
    # address = request.data['address']
    shop = request.data['data']
    shop = json.loads(shop)
    print(type(shop))
    shop['code'] = shopCode()
    shop['area'] = models.Area.objects.get(id=int(shop['area']))
    shop['product_type'] = models.ProductType.objects.get(id=int(shop['product_type']))
    shop['user'] = user
    print((shop))
    
    try :
        shop = models.Shop.objects.create(**shop)

        if shop:
            http_status = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_400_BAD_REQUEST

    except IOError as err:
        print(err)
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
    remark = request.data['remark']
    invoice_no = invoice_code()

    invoice = models.InputInvoice.objects.create(
        shop=shop,
        invoice_no=invoice_no,
        remark=remark,
    )

    # create product and input data
    products = json.loads(request.data['products'])
    for key, product in products.items():

        total_price += product['total']
        total_discount += product['discount']

        discount = product['discount']
        quantity = product['unit']
        unit_price = product['price']

        del product['total']
        del product['discount']
        product['shop'] = shop
        cats = product['category']
        print(cats, type(cats))

        product['category'] = models.ProductCategory.objects.get(
            id=int(product['category']))
        product['code'] = product_code(cats, shop)

        product = models.Product.objects.create(**product)
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

    InvoiceData = inputInvoiceData(invoiceSerializer)

    return Response(status=status.HTTP_200_OK, data=InvoiceData)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((IsAuthenticated,))
def shopProducts(request):
    http_status = status.HTTP_200_OK

    user = User.objects.get(username=request.user.username)
    shop = models.Shop.objects.get(user=user)

    productQuery = models.Product.objects.filter(
        shop=shop).order_by('-updated_at')
    productSerializers = serializers.ProductSerializer(productQuery, many=True)

    productData = []

    for product in productSerializers.data:
        product = dict(product)
        product_cats = models.ProductCategory.objects.get(
            id=int(product['category']))
        cats = serializers.ProductCategorySerializer(product_cats).data
        product['category'] = cats
        productData.append(product)

    return Response(status=http_status, data=productData)

# Product Methods


@csrf_exempt
@api_view(["POST", ])
@permission_classes((IsAuthenticated,))
def editProduct(request):
    http_status = status.HTTP_200_OK
    edit = request.data['product']
    product = json.loads(edit)
    del product['total']

    models.Product.objects.filter(id=int(product['id'])).update(**product)

    return Response(status=http_status)


@csrf_exempt
@api_view(["POST", ])
@permission_classes((IsAuthenticated,))
def addProduct(request):
    http_status = status.HTTP_200_OK

    id = int(request.data['id'])
    unit = int(request.data['unit'])
    remark = request.data['remark']

    if unit <= 0:
        http_status = status.HTTP_400_BAD_REQUEST

    else:
        user = User.objects.get(username=request.user.username)
        shop = models.Shop.objects.get(user=user)
        total_discount = 0
        invoice_no = invoice_code()

        update = models.Product.objects.filter(
            id=id).update(unit=F("unit")+unit)
        if update:
            product = models.Product.objects.get(id=id)

        invoice = models.InputInvoice.objects.create(
            shop=shop,
            invoice_no=invoice_no,
            total_price=(unit*product.price),
            discount=total_discount,
            remark=remark,
            type=2
        )

        input_data = models.InputData.objects.create(
            invoice=invoice,
            product=product,
            quantity=unit,
            unit_price=product.price,
            discount=0

        )

        if input_data:
            http_status = status.HTTP_201_CREATED

    return Response(status=http_status)


@csrf_exempt
@api_view(["POST", ])
@permission_classes((IsAuthenticated,))
def shopFilterInvoice(request):

    user = User.objects.get(username=request.user.username)
    shop = models.Shop.objects.get(user=user)
    type = int(request.data['type'])
    
    from_date = request.data['from']
    to_date = request.data['to']
    filters = {}
    filters['shop'] = shop

    if type != 0:
        filters['type'] = type


    if from_date == "" and to_date != "":
        filters['shop'] = shop
        # print(to_date)
        # from_date = datetime.strptime("2000-01-01", '%Y-%m-%d')
        # from_date = str(from_date).split(" ")[0]
        to_date = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)
        to_date = str(to_date).split(" ")[0]
        filters['created_at__range'] = ("2000-01-01", to_date)

    elif from_date != "" and to_date == "":

        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        from_date = str(from_date).split(" ")[0]
        to_date = datetime.now() + timedelta(days=1)
        to_date = str(to_date).split(" ")[0]
        
        filters['created_at__range'] = (from_date, to_date)


    
    invoiceQuery = models.InputInvoice.objects.filter(**filters).order_by('-updated_at')
    
    invoiceSerializer = serializers.InputInvoiceSerializer(
        invoiceQuery, many=True)

    InvoiceData = inputInvoiceData(invoiceSerializer)

    return Response(status=status.HTTP_200_OK, data=InvoiceData)





