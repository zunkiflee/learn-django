from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home, name='home-page'),
    path('about/', About, name='about-page'),
    path('contact/', Contact, name='contact-page'),
  	path('truk/', Truk, name='truk-page'),
  	path('addproduct/', AddProduct, name='addproduct-page'),
  	path('allproduct/', Productall, name='allproduct-page'),
  	path('register/', Register, name='register-page'),
  	path('test/', Test, name='test-page'),
  	path('addtocart/<int:pid>/', AddtoCart,name='addtocart-page'),
  	path('mycart/', MyCart, name='mycart-page'),
    path('mycart/edit/', MyCartEdit, name='mycartedit-page'),
    path('checkout/', Checkout, name='checkout-page'),
    path('orderlist/', OrderListPage, name='orderlist-page'),
    path('allorderlist/', AllOrderListPage, name='allorderlist-page'),
    path('uploadslip/<str:orderid>/', UpoadSlip, name='uploadslip-page'),
    path('updatestatus/<str:orderid>/<str:status>', UpdatePaid, name='updatestatus'),
    path('updatetacking/<str:orderid>', UpdateTracking, name='updatetacking'),
    path('myorder/<str:orderid>', MyOrder, name='myorder-page'),
]