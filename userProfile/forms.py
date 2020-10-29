from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

# This is the form for the user profile.
class userProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'street_address1', 'street_address2','town_city', 'postcode', 'country']