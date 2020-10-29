from django.urls import path, include
from . import views
from accounts.views import index, logout, login, registration

# URLpatterns for the accounts app.
urlpatterns = [
    path('', index, name="index"),
    path('logout/', logout, name="logout"),
    path('login/', login, name="login"),
    path('register/', registration, name="register"),
]