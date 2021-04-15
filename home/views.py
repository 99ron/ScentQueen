from django.shortcuts import render
from django.shortcuts import render, redirect

from store.models import *
from store.utils import cookieCart, cartData


# Views for the home app.

""" Simply returns the home.html file """
def home(request):
	
	data = cartData(request)
	cartItems = data['cartItems']

	context = {'cartItems': cartItems}
	return render(request, "home.html", context)


""" A view to show the about us page """

# This renders the user to the 'about us' page.
def about(request):
	
	data = cartData(request)
	cartItems = data['cartItems']

	context = {'cartItems': cartItems}

	return render(request, "about-us.html", context)


