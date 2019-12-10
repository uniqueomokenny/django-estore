from django.urls import path
from . import views 


app_name = 'store'

urlpatterns = [
    path('', views.item_list, name='item-list'),
    path('detail/', views.item_detail, name='item-detail'),
    path('checkout/', views.checkout, name='checkout'),
]
