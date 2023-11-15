from django.urls import path
from AppShop import views

app_name = 'AppShop'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('product-details/<pk>', views.ProductDetails.as_view(), name='product_details'),
]
