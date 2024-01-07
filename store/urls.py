"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('auth-login', views.loginUser, name='login-api'),


    path('get-product-type', views.getProductType, name='get-product-type-api'),
    path('get-product-category', views.getProductCategory,
         name='get-product-category-api'),

    path('store-product', views.shopProducts, name='get-store-product-api'),
    path('store-invoice', views.shopInvoice, name='get-shop-invoice-api'),
    path('store-filter-invoice', views.shopFilterInvoice, name='filter-shop-invoice-api'),
    path('create-input-data', views.createInputData,
         name='create-input-data-api'),
    
    
    # product api
    path('add-product', views.addProduct, name='add-product-api'),
    path('edit-product', views.editProduct, name='edit-product-api')
]
