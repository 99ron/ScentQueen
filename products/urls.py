from django.urls import path
from .views import all_products, categories


urlpatterns = [
    path('show_categories', categories, name="categories"),
    path('all_products', all_products, name="products"),
    ]