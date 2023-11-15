from django.urls import path
from AppPayment import views

app_name = 'AppPayment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('status/', views.complete, name='status'),
    path('purchase/<val_id>/<tran_id>', views.purchase, name='purchase'),
    path('orders/', views.order_view, name='orders'),
]
