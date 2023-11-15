from django.shortcuts import render
from AppShop.models import Catergory, Product
# Import Views
from django.views.generic import ListView, DetailView
# Mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomePage(ListView):
    model = Product
    template_name = 'AppShop/homepage.html'


class ProductDetails(LoginRequiredMixin,DetailView):
    model = Product
    template_name = 'AppShop/product_details.html'
    