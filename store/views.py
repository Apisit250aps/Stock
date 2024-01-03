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

from django.db.models import Q

from datetime import datetime

from . import models


# Create your views here.


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
