import json
from .models import *
from userProfile.models import UserProfile

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]["quantity"],
                'get_total':total
                }
                
            items.append(item)
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}
    
def cartData(request):
    if request.user.is_authenticated:
        customer = UserProfile.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}
    
def guestOrder(request, data):
    print("User is not logged in.")
        
    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    
    cookieData = cookieCart(request)
    items = cookieData['items']
    
    # This is the user id for an anon account I've created.
    customer = UserProfile.objects.get(user=3)

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )
    
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            )
    return customer, order