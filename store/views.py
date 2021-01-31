from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder
from userProfile.models import UserProfile
# Views for the store, cart and checkout.

def store(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    context = { 'products':products, 'cartItems':cartItems}
    return render(request, 'store.html', context)



def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)
    
    
    
def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)
    


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action: ', action)
    print('productId: ', productId)
    
    customer = UserProfile.objects.get(user=request.user)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
            orderItem.quantity = (orderItem.quantity -1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)
    
    

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        
        customer = UserProfile.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
    
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address1=data['shipping']['address1'],
        address2=data['shipping']['address2'],
        city=data['shipping']['city'],
        county=data['shipping']['county'],
        postcode=data['shipping']['postcode'],
        )
      
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if str(total) == str(order.get_cart_total):
        order.complete = True
    order.save()
        
    return JsonResponse('Payment Complete!', safe=False)