from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def loginPage(request):
    
    return render(request, 'auth/login.html')

def registerPage(request):
    
    return render(request, 'auth/register.html')



# Customer Page
@login_required()
def indexPage(request):
    
    return render(request, 'customer/index.html')

@login_required()
def shopCreatePage(request):
    
    return render(request, 'customer/shop.html')


@login_required()
def accountSettingPage(request):
    
    return render(request, 'customer/account-setting.html')


# 

@login_required()
def productsPage(request):
    
    return render(request, 'store/products.html')

@login_required()
def invoicesPage(request):
    
    return render(request, 'store/invoices.html')

@login_required()
def inputPage(request):
    
    return render(request, 'store/input.html')


@login_required()
def shopPage(request):
    
    return render(request, 'store/shop.html')
