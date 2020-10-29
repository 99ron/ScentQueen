from django.test import TestCase, Client
from django.http import HttpRequest
from django.urls import reverse
from .forms import UserRegistrationForm
from .views import *

# Test for the accounts app

class Accounts_App_Tests(TestCase):
    
    # Checks that the function to go 'home' is working.
    def test_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class Setup_Class(TestCase):
    
    def setUp(self):
        # Sets up a user for testing
        self.user = User.objects.create(email="user@testing.com", username="TestUser", password1="password", password2="password")

        
class Registration_Form_Test(TestCase):
    
    
    # Checks for a valid form submission
    def test_reg_form_valid(self):
        form_data = {'email': 'user@testing.com', "username": "user", 'password1' : 'password', 'password2' : 'password'}
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    
    # Checks for a invalid form submission
    def test_reg_form_invalid(self):
        form_data = {'email' : '', 'username' : 'user', 'password1' : 'pass', 'password2' : 'password2'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        

# Testing a view
class Accounts_App_Views(TestCase):
    
    # Check that credentials are correct and the template correct template loads. 
    def test_login_view(self):
        self.client.login(username='TestUser', password='password')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')