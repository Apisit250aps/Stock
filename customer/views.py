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


from django.contrib.staticfiles import finders


import json
# Create your views here.


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

    # get thai province file
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
        models.Customer.objects.filter(user=user).update(**customer_update)
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
    data=serializers.CustomerSerializer(customer).data
    
    
    
    return Response(data, http_status)