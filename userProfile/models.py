from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# User profile model.

# This makes it so the phone number can only have numbers entered.
numbersOnly = RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="users",on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=12, blank=False, verbose_name="First Name") 
    last_name = models.CharField(max_length=20, blank=False, verbose_name="Last Name")
    phone_number = models.CharField(max_length=14, validators=[numbersOnly], blank=False, verbose_name="Phone Number")
    street_address1 = models.CharField(max_length=40, blank=False, verbose_name="First line of Address")
    street_address2 = models.CharField(max_length=40, blank=True, verbose_name="Second line of Address")
    postcode = models.CharField(max_length=50, blank=False, verbose_name="Postcode")
    town_city = models.CharField(max_length=40, blank=False, verbose_name="Town/City")
    country = models.CharField(max_length=50, blank=False, verbose_name="Country")
    employee = models.BooleanField(default=False)
    
    def __str__(self):
        return "{0}".format(self.user)