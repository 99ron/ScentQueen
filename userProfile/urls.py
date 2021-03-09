from django.urls import path, include
from .views import user_profile, my_orders
from . import views

# URLpattern for the profiles app.
urlpatterns = [
    path('profile/', user_profile, name="profile"),
    path('profile/my-orders', my_orders, name="my_orders"),
    path('hide_order/<int:orderId>', views.hide_order, name="hide_order"),
]