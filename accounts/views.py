from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm
from userProfile.models import UserProfile, UserAddress
from userProfile.urls import user_profile 


# Views for the accounts app.

def index(request):
    """Return the home html file"""
    return render(request, 'home.html')


@login_required    
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have logged out succesfully")
    return redirect(reverse('index'))
    

def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    """If this is a post request it confirms that the user credentials are correct and exists."""
    if request.method=="POST":
        login_form = UserLoginForm(request.POST)
        
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have succesfully logged in!")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form" : login_form})




def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
        
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
          
        if registration_form.is_valid():
            registration_form.save()
            
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1']) 

            if user:
                auth.login(user=user, request=request)
                
                """ Creates a blank profile page """
                makeProfile(request)
                
                """This sends the user to the profile page to fill out their information."""
                messages.success(request, "You have succesfully registered")
                return redirect(user_profile)
            else:
                messages.error(request, "Unable to register your account at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'registration.html', {
        "registration_form" : registration_form})


def makeProfile(request):
    """ This creates an empty profile for the user to fill out """
    upr = UserProfile()
    upr.user = request.user
    upr.save()
    
    """ This associates the newly created profile user table to the address table"""
    uar = UserAddress()
    uar.person = UserProfile.objects.get(user=upr.user)
    uar.save()