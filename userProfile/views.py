from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from home.views import home
from .forms import userProfileForm

# User Profile Function
@login_required
def user_profile(request):
    
    '''
    This gets the profile page for the logged in User.
    If it doesn't exist it'll return to the homepage.
    '''
    try:
        user = UserProfile.objects.get(pk=request.user.id)
    except Exception as e:
        messages.error(request, "No profile found, please contact the company: " + str(e))
        return render(request, 'home.html')       
    
    if request.method == 'GET':
        
        """The user's profile"""
        
        form = userProfileForm(instance=user)
        
    else:
        # Requests the form and files data.
        form = userProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            # Sets the unique user profile instance up. 
            up = user
            
            try:
                up.first_name = form.cleaned_data['first_name']
                up.last_name = form.cleaned_data['last_name']
                up.phone_number = form.cleaned_data['phone_number']
                up.town_city = form.cleaned_data['town_city']
                up.street_address1 = form.cleaned_data['street_address1']
                up.street_address2 = form.cleaned_data['street_address2']
                up.postcode = form.cleaned_data['postcode']
                up.country = form.cleaned_data['country']
                
                up.save()
                messages.success(request, "Your profile was updated successfully!")
                return render(request, 'home.html')
                
            except Exception as e:
                # If an error occurs it throws up a message and asks to retry.
                messages.error(request, "Failed to update: " + str(e))
                return render(request, 'profile.html', {'form' : form, 'profile' : user})
                
    return render(request, 'profile.html', {'form' : form, 'profile' : user})