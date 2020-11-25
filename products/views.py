from django.shortcuts import render
from .models import Product

# Products app views listed below.

# Renders the page for the user to choose between wax melts and car scents.
def categories(request):
    return render(request, 'categories.html')


# This renders a page with all items for sale.
def all_products(request):
    products = Product.objects.all()
    return render(request, "products.html", {'products':products})