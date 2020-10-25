from django.shortcuts import render

# Views for the home app.

""" Simply returns the home.html file """
def home(request):
    return render(request, "home.html")
