from django.urls import path
from AppLogin import views

app_name = 'AppLogin'


urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('profile/', views.user_profile, name='profile'),
]
