from django.urls import path, include
from .views import user_profile

# URLpattern for the profiles app.
urlpatterns = [
    path('profile/', user_profile, name="profile"),
]