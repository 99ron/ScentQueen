from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, UserAddress
from django.contrib.auth.decorators import login_required
from home.views import home
from .forms import userProfileForm, userAddressForm

# User Profile Function
@login_required
def user_profile(request):
    
    '''
    This gets the profile page for the logged in User.
    If it doesn't exist it'll return to the homepage.
    '''
    
    if request.user.is_authenticated:
    
        try:
            user = UserProfile.objects.get(pk=request.user.id)
           
        except Exception as e:
            messages.error(request, "No profile was found, please contact the company.")
            return render(request, 'home.html')       
        
        if request.method == 'GET':
            
            """The user's profile"""
            formUser = userProfileForm(instance=user)
            
            # This matches the logged in user to the address table which then renders the form with the correct data.
            try:
                address = UserAddress.objects.get(person=user)
                formAddress = userAddressForm(instance=address)
            except:
                formAddress = userAddressForm()   
                
        else:
            # Requests the form and files data.
            formUser = userProfileForm(request.POST)
            formAddress = userAddressForm(request.POST)
            
            if formUser.is_valid() and formAddress.is_valid():
                
                # Sets the unique user profile instance up. 
                # address = UserAddress.objects.get(person=user)
                up = user
                ua = formAddress
                try:
                    up.first_name = formUser.cleaned_data['first_name']
                    up.last_name = formUser.cleaned_data['last_name']
                    up.phone_number = formUser.cleaned_data['phone_number']
                    up.gender = formUser.cleaned_data['gender']
                    up.email = formUser.cleaned_data['email']
                    
                    ua.town_city = formAddress.cleaned_data['town_city']
                    ua.street_address1 = formAddress.cleaned_data['street_address1']
                    ua.street_address2 = formAddress.cleaned_data['street_address2']
                    ua.postcode = formAddress.cleaned_data['postcode']
                    ua.country = formAddress.cleaned_data['country']
  
                    up.save()
                    ua.save()
                    
                    messages.success(request, "Your profile was updated successfully!")
                    return redirect(user_profile)
                    
                except Exception as e:
                    # If an error occurs it throws up a message and asks to retry.
                    messages.error(request, "Failed to update: " + str(e))
                    return render(request, 'profile.html', {'formUser' : formUser, 'formAddress' : formAddress, 'profile' : user})
                    
        return render(request, 'profile.html', {'formUser' : formUser,'formAddress' : formAddress, 'profile' : user})
    
    # If the user isn't logged in then redirect them to the log in page.
    else:
        return render(request, 'login.html')
        

# Will pull through orders when the database is set up for it. Now it'll simply render a page.
@login_required
def my_orders(request):
    
    
    return render(request, 'my-orders.html')