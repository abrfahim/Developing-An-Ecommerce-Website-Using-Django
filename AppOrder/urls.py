from django.urls import path
from AppOrder import views

app_name = 'AppOrder'


urlpatterns = [
    path('add/<pk>', views.add_to_cart, name='add'),
    path('remove/<pk>', views.remove_cart_item, name='remove'),
    path('cart/', views.cart_veiw, name='cart'),
    path('increase/<pk>', views.increase_item, name='increase'),
    path('decrease/<pk>', views.decrease_item, name='decrease'),

]
