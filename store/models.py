from django.db import models
from userProfile.models import UserProfile

# models for the products

PRODUCT_CATEGORY = (
    ("WaxMelts", "Wax Melts"),
    ("CarScents", "Car Scents"),
    )


class Product(models.Model):
    name = models.CharField(max_length=254, default='')
    description = models.TextField()
    product_type = models.CharField(max_length=50, choices= PRODUCT_CATEGORY)
    price =  models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)
        
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

  
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address1 = models.CharField(max_length=200, null=False)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=False)
    county = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=8, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Order: {0} by {1}".format(self.order, self.customer)
        

class ProcessedOrders(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=80, null=False)
    email_address = models.EmailField(max_length=200, null=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=3, null=False)
    posted = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=False, null=True)
    
    def __str__(self):
        return "Customer: {0}, Order Number: {1}, Posted?: {2}".format(self.customer, self.order, self.posted)