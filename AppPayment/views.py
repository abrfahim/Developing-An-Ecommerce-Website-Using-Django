from math import log
from multiprocessing import context
from django.shortcuts import render, HttpResponseRedirect, redirect
from AppPayment.models import BillingAddress
from AppOrder.models import Order, Cart
from AppPayment.forms import BillingForm

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request,f"Shipping address saved successfully!")
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    diction = {'form': form, 'order_items': order_items, 'order_total': order_total, 'saved_address': saved_address}
    return render(request, 'AppPayment/checkout.html', context=diction)



@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    
    if not saved_address.is_fully_filled():
        messages.info(request, "Plese Complete your shipping address!")
        return redirect('AppPayment:checkout')

    if not request.user.profile.is_fully_filled():
        messages.info(request, "Plese Complete your Profile!")
        return redirect('AppLogin:profile')
    
    
    # SSL-Authorization
    store_id = 'thevi6552744e8167c'
    API_key = 'thevi6552744e8167c@ssl'  
    
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)

    #set urls
    status_url = request.build_absolute_uri(reverse('AppPayment:status'))
    
    mypayment.set_urls(
        success_url= status_url, 
        fail_url=status_url, 
        cancel_url=status_url, 
        ipn_url= status_url,
    )
    
    
    #product integration
    
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()
    
    mypayment.set_product_integration(
        total_amount=Decimal(order_total),
        currency='BDT', 
        product_category='Mixed', 
        product_name= order_items , 
        num_of_item= order_items_count, 
        shipping_method='Couriar', 
        product_profile='None',
    )
    
    # customer info
    current_user = request.user
    
    mypayment.set_customer_info(
        name= current_user.profile.full_name,
        email= current_user.email ,
        address1= current_user.profile.address_1,
        address2= current_user.profile.address_1,
        city= current_user.profile.city,
        postcode= current_user.profile.zip_code,
        country= current_user.profile.country,
        phone= current_user.profile.phone,
    )



    mypayment.set_shipping_info(
        shipping_to = current_user.profile.full_name,
        address = saved_address.address,
        city = saved_address.city,
        postcode = saved_address.zipcode,
        country = saved_address.country,
    )
    
    response_data = mypayment.init_payment()
    print(response_data)
    
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST   
        status = payment_data['status']
        
        
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, 'Your Payment Completed Successfully! You will be redirected to homepage after 3 seconds!')
            return HttpResponseRedirect(reverse('AppPayment:purchase', kwargs={'val_id': val_id, 'tran_id':tran_id,}))
        
        elif status == 'FAILED':
            messages.warning(request, 'Your Payment Failed!')
            
        else:
            messages.info(request, '')
        
    diction = {}
    return render(request, 'AppPayment/complete.html', context = diction)


@login_required
def purchase(request, val_id, tran_id):
    
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orderId = orderId
    order.paymentId = val_id
    order.save()
    
    cart_items = Cart.objects.filter(user = request.user, purchased = False)
    
    for item in cart_items:
        item.purchased = True
        item.save()
    
    diction = {}
    return HttpResponseRedirect(reverse('AppShop:homepage'))



@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered = True)
        diction = {'orders': orders}
        
    except:
        messages.warning(request,  f"You don't have any active order")
        return redirect('AppShop:homepage')
    return render(request, 'AppPayment/order.html',context = diction) 