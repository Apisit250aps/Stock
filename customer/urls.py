from django.urls import path

from . import views as api

urlpatterns = [
    path('province', api.getProvince, name='get-province'),
    path('district', api.getDistrict, name='get-district'),
    path('tambon', api.getTambon, name='get-tambon'),

    path('update', api.createCustomer, name='update-customer'),
    path('get', api.getCustomerSelf, name='get-customer'),

    path('action-cart', api.actionCart, name='action-cart-api'),
    path('cart-list', api.cartList, name='cart-list-api'),
    path('checkout', api.checkout, name='check-out-api'),
    path('order', api.customerOrder, name='order-api'),

]
