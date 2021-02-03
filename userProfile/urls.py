from django.urls import path, include
from .views import user_profile, my_orders

# URLpattern for the profiles app.
urlpatterns = [
    path('profile/', user_profile, name="profile"),
    path('profile/my-orders', my_orders, name="my_orders"),
]