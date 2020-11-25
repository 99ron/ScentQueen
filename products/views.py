from django.shortcuts import render
from .models import Product

# View to show all the products.
def all_products(request):
    products = Product.objects.all()
    return render(request, "products.html", {'products':products})