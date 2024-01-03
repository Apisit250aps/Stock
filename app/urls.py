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
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.indexPage, name='index-page'),
    path('auth-login/', views.loginPage, name='login-page'),
    path('auth-register/', views.registerPage, name='register-page'),
    path('auth-logout/', lambda request: redirect("index-page")
         if logout(request) else redirect("index-page"), name='logout'),

    path('store/products', views.productsPage, name='products-page'),
    path('store/invoices', views.invoicesPage, name='invoices-page'),
    path('store/input', views.inputPage, name='input-page'),
]