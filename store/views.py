from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import cookieCart, cartData, guestOrder
from userProfile.models import UserProfile
# Views for the store, cart and checkout.


# Simple function to order the shop results
def shop_sort_by(sort_by):
    
    if sort_by == "Wax Melts":
        # If sort_by contains WaxMelts it'll display the results.
        order_list = Product.objects.all().order_by('-product_type')
    
    elif sort_by == "Car Scents":
        # If sort_by contains Newest it'll display the results Newest first.
        order_list = Product.objects.all().order_by('product_type')
    
    return order_list


def store(request):
    
    sort_by = request.GET.get('orderSortBy')
    
    if sort_by == None:
        order_list = Product.objects.all()
    else:
        # Passes the variable to the function so it can be filtered above. 
        order_list = shop_sort_by(sort_by)
    
    
    data = cartData(request)
    cartItems = data['cartItems']
    
    # This is to limit the amount that's shown on a page using pagination only showing 9 per page.
    page = request.GET.get('page', 1)
    paginator = Paginator(order_list, 9)
    
    try:
        shop_list = paginator.page(page)
    except PageNotAnInteger:
        shop_list = paginator.page(1)
    except EmptyPage:
        shop_list = paginator.page(paginator.num_pages)
    
    

    context = { 'products':order_list, 'cartItems':cartItems, 'sort_by':sort_by, 'shop_list':shop_list}
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
    
    # This checks that the price hasn't been manipulated by checking the total on the page compared to
    # the orders total cart cost.
    if str(total) == str(order.get_cart_total):
        order.complete = True
    order.save()

    return JsonResponse('Payment Complete!', safe=False)
    