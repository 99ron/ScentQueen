from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# User profile model.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    )

# This makes it so the phone number can only have numbers entered.
numbersOnly = RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=12, blank=False, verbose_name="First Name") 
    last_name = models.CharField(max_length=20, blank=False, verbose_name="Last Name")
    phone_number = models.CharField(max_length=14, validators=[numbersOnly], blank=False, verbose_name="Phone Number")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False, default='')
    email = models.EmailField(max_length=200)
    employee = models.BooleanField(default=False)
    
    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)
        

class UserAddress(models.Model):
    person = models.ForeignKey(UserProfile, related_name="userProfile", on_delete=models.CASCADE, null=True, blank=True)
    street_address1 = models.CharField(max_length=40, blank=False, verbose_name="First line of Address")
    street_address2 = models.CharField(max_length=40, blank=True, verbose_name="Second line of Address")
    postcode = models.CharField(max_length=50, blank=False, verbose_name="Postcode")
    town_city = models.CharField(max_length=40, blank=False, verbose_name="Town/City")
    country = models.CharField(max_length=50, blank=False, verbose_name="Country")
    
    def __str__(self):
        return "{0}".format(self.person)