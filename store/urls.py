from django.urls import path
from . import views 


app_name = 'store'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug>', views.ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>', views.remove_single_item_from_cart, name='remove-single-item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-summary/', views.OrderSummary.as_view(), name='order-summary'),
]
