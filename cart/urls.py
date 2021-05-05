from django.urls import path

from . import views

urlpatterns = [
    path('',views.cart_detail,name='cart_detail'),
    path('success/',views.success,name='success')
]