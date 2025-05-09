from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dishes/', dishes_list, name='dishes_list'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout_view, name='checkout_view'),
    path('payment/', payment_view, name='payment_view'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),

]
