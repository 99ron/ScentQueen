from django.urls import path, include
from django.contrib import admin
from .views import contact

# URLpatterns for the contact us app.
urlpatterns = [
    path('contact/', contact, name="contact"),
]