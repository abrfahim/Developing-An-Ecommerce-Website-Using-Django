from django.shortcuts import render, get_object_or_404, redirect
# Authenticator
from django.contrib.auth.decorators import login_required
# Messages
from django.contrib import messages

from AppShop.models import Product
from AppOrder.models import Cart, Order

# Create your views here.

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user = request.user, purchased = False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, 'Qunatity Updated Successfully!')
            return redirect('AppShop:homepage')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, 'This item added to Cart!')
            return redirect('AppShop:homepage')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, 'This item added to Cart!')
        return redirect('AppShop:homepage')
    
    
@login_required
def cart_veiw(request):
    carts = Cart.objects.filter(user = request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered = False)
    if carts.exists() and orders.exists():
        # converted to tuple to list for accessing
        order = orders[0]
        diction = {'order': order, 'carts':carts}
        return render(request, 'AppOrder/cart.html', context=diction)
    else:
        messages.warning(request, "You don't have any item in your cart !")
        return redirect('AppShop:homepage')
    
@login_required
def remove_cart_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        # converting tuple to list
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item=order_item[0]    #converted the item to list from tuple
            order.orderitems.remove(order_item) #remove from order
            order_item.delete() #delete from cart
            messages.info(request, 'Item Removed successfully!')
            return redirect('AppOrder:cart')
        else:
            messages.info(request,'Now, This item is not available in your Cart!')
            return redirect('AppShop:homepage')
    else:
        messages.info(request, 'You have no order')
        return redirect('AppShop:homepage')


@login_required
def increase_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0] #converted to list for accessibility
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity>=1:
                order_item.quantity +=1
                order_item.save()
                messages.info(request, f"{item.name} has been updated!")
                return redirect('AppOrder:cart')
        else:
            messages.info(request,f"{item.name} is not in your cart!")
    else:
        messages.info(request, "You don't have any order")
        return redirect('AppOrder:cart')
    
    
@login_required
def decrease_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0] #converted to list for accessibility
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request, f"{item.name} has been updated!")
                return redirect('AppOrder:cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} has been removed from cart!")
                return redirect('AppOrder:cart')
        else:
            messages.info(request,f"{item.name} is not in your cart!")
            return redirect('AppShop:homepage')
    else:
        messages.info(request, "You don't have any order")
        return redirect('AppShop:homepage')