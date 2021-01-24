from django.shortcuts import render

# Views for the store, cart and checkout.

def store(request):
    context = {}
    return render(request, 'store.html', context)

def cart(request):
    context = {}
    return render(request, 'cart.html', context)
    
def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)