from django.db.models import Q, F
from django.contrib.auth.models import User
from . import models
from . import serializers
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from store.models import (
    Product,
    ProductCategory,
    Shop,
    InputInvoiceCounter
)

from store.serializers import (
    ProductCategorySerializer,
    ProductSerializer
)

from django.contrib.staticfiles import finders

from datetime import datetime
from datetime import timedelta
import json
# Create your views here.


def invoice_code():

    date = datetime.today().date().__str__().replace("-", "")
    if InputInvoiceCounter.objects.filter(on_date=date).count() == 0:
        InputInvoiceCounter.objects.create(on_date=date)
    else:
        InputInvoiceCounter.objects.filter(
            on_date=date).update(no=F('no')+1)
    count = InputInvoiceCounter.objects.get(on_date=date)

    return date+"{0:04}".format(int(count.no))


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def getProvince(request):
    data = {}
    msg = 'already get thai province'
    http_status = status.HTTP_200_OK

    # get thai province file
    result = finders.find('data/thai_province.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    data['province'] = province.keys()

    return Response({'status': True, 'message': msg, 'data': data}, status=http_status)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getDistrict(request):
    data = {}
    msg = 'already get thai district'
    http_status = status.HTTP_200_OK

    # get thai province file
    result = finders.find('data/thai_province.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    province_selected = request.data['province']
    data['district'] = province[province_selected].keys()

    return Response({'status': True, 'message': msg, 'data': data}, status=http_status)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getTambon(request):
    data = {}
    msg = 'already get thai tambon'
    http_status = status.HTTP_200_OK

    # get thai province file-
    result = finders.find('data/thai_province.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    province_selected = request.data['province']
    district_selected = request.data['district']

    data['tambon'] = province[province_selected][district_selected]

    return Response({'status': True, 'message': msg, 'data': data}, status=http_status)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def createCustomer(request):
    http_status = status.HTTP_200_OK
    user = User.objects.get(username=request.user.username)
    data = request.data['customer']
    data = json.loads(data)

    user_update = {}
    customer_update = {}
    customer_update['contact'] = data['first_name']+" "+data['last_name']

    user_update['first_name'] = data['first_name']
    user_update['last_name'] = data['last_name']
    del data['first_name']
    del data['last_name']

    for i, o in data.items():

        customer_update[i] = o

    print(user_update)
    print(customer_update)

    try:
        User.objects.filter(id=user.id).update(**user_update)
        models.Customer.objects.filter(
            user=user).update(**customer_update)

        customer = models.Customer.objects.get(user=user)
        cart = models.Cart.objects.create(customer=customer)
        http_status = status.HTTP_200_OK
    except IOError as err:
        print(err)
        http_status = status.HTTP_400_BAD_REQUEST

    return Response(
        status=http_status
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getCustomerSelf(request):
    http_status = status.HTTP_200_OK
    user = User.objects.get(username=request.user.username)
    customer = models.Customer.objects.get(user=user)
    data = serializers.CustomerSerializer(customer).data

    return Response(data, http_status)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def actionCart(request):
    http_status = status.HTTP_200_OK
    user = User.objects.get(username=request.user.username)
    customer = models.Customer.objects.get(user=user)
    if models.Cart.objects.filter(customer=customer).count() != 0:
        cart = models.Cart.objects.get(customer=customer)
    else :
        cart = models.Cart.objects.create(customer=customer)
    action = int(request.data['action'])
    product = int(request.data['product'])
    unit = int(request.data['unit']) * action

    product = Product.objects.get(id=product)

    if models.CartItem.objects.filter(cart=cart, product=product).count() == 0:
        models.CartItem.objects.create(cart=cart, product=product, unit=unit)
    else:
        models.CartItem.objects.filter(
            cart=cart, product=product).update(unit=F('unit')+unit)

    if models.CartItem.objects.get(cart=cart, product=product).unit == 0:

        models.CartItem.objects.filter(cart=cart, product=product).delete()

    http_status = status.HTTP_201_CREATED

    return Response(status=http_status)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def cartList(request):
    http_status = status.HTTP_200_OK
    user = User.objects.get(username=request.user.username)
    customer = models.Customer.objects.get(user=user)
    cart = models.Cart.objects.get(customer=customer)
    cartData = {}
    cart_items = serializers.CartItemSerializer(
        models.CartItem.objects.filter(cart=cart).order_by('-id'), many=True).data

    for item in cart_items:
        item = dict(item)
        product = Product.objects.get(id=int(item['product']))

        item['product'] = dict(ProductSerializer(product).data)
        shop = Shop.objects.get(id=int(item['product']['shop']))
        item['shop_id'] = shop.id

        if shop.name in cartData:
            cartData[shop.name].append(item)
        else:
            cartData[shop.name] = [item]

    cartArray = []
    for i, o in cartData.items():
        cartArray.append({
            "shop": i,
            "products": o})
    
    cartArray

    return Response(status=http_status, data=cartArray)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def checkout(request):
    http_status = status.HTTP_200_OK
    shop_id = int(request.data['shop'])
    shop = Shop.objects.get(id=shop_id)
    user = User.objects.get(username=request.user.username)
    customer = models.Customer.objects.get(user=user)
    cart = models.Cart.objects.get(customer=customer)
    
    

    product = request.data['product']
    product = json.loads(product)

    print(type(product))
    try :
        
        invoice_no = invoice_code()

        invoice = models.OutputInvoice.objects.create(
            shop=shop,
            customer=customer,
            invoice_no=invoice_no,
            discount=0,
            remark="-"
        )

        for item in product.values():
            print(item)
            product = Product.objects.get(id=int(item['product']))
            unit = item['value']

            output_data = models.OutputData.objects.create(
                invoice=invoice,
                product=product,
                quantity=unit,
                unit_price=product.price,
                discount=0
            )
            
            if output_data:
                models.CartItem.objects.filter(
                    cart=cart,
                    product=product
                ).delete()
            
        models.Order.objects.create(
            customer=customer,
            shop=shop,
            invoice=invoice,
            status=1
        )
        http_status = status.HTTP_201_CREATED
    except :
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response(status=http_status)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def customerOrder(request):
    http_status = status.HTTP_200_OK
    user = User.objects.get(username=request.user.username)
    customer = models.Customer.objects.get(user=user)

    orderQ = models.Order.objects.filter(customer=customer).order_by('-status', '-id')
    orderS = serializers.OrderSerializer(orderQ, many=True).data
    orderD = []
    
    for order in orderS:
        order = dict(order)
        shop = Shop.objects.get(id=int(order['shop']))
        invoice = models.OutputInvoice.objects.get(id=int(order['invoice']))
        data = []
        output = serializers.OutputDataSerializer(models.OutputData.objects.filter(invoice=invoice), many=True).data
        for pro in output:
            pro = dict(pro)
            pro['product']  = Product.objects.get(id=int(pro['product'])).name
            data.append(pro)
            
        # output['product'] = Product.objects.get(id=int(output['product'])).name
        order['status'] = map_choice(models.ORDER_STATUS, order['status'])
        order['shop'] = shop.name
        order['invoice'] = invoice.invoice_no
        
        order['product'] = data
        orderD.append(order)
    
    return Response(
        orderD, status=http_status
    )
    

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def cancelOrder(request):
    order = int(request.data['order'])
    models.Order.objects.filter(id=order).update(status=4)
    return Response(status=200)


def map_choice(choice, value):
    for i in choice:
        if i[0] == value:
            return i[1]
