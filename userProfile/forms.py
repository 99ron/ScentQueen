from django import forms
from crispy_forms.helper import FormHelper
from .models import UserProfile, UserAddress
# from django.contrib.auth.models import User


# This is the form for the user profile.
class userProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'gender' ]
        widgets = {'gender':forms.RadioSelect}


# This is the form for the user's address.        
class userAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['street_address1', 'street_address2','town_city', 'postcode', 'country']