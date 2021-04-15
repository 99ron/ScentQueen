from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm
from userProfile.models import UserProfile, UserAddress
from userProfile.urls import user_profile 

# Used for the password reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


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
    
    """ This associates the newly created profile usertable to the address table"""
    uar = UserAddress()
    uar.person = UserProfile.objects.get(user=upr.user)
    uar.save()


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/password_reset_email.html"
					context = {
					"email":user.email,
					'domain':get_current_site(request),
					'site_name': 'The Scent Queen',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
					email = render_to_string(email_template_name, context)
					
					try:
						send_mail(subject, email, 'info.thescentqueen@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
					
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset_form.html", context={"password_reset_form":password_reset_form})