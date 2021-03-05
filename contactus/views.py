from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect 
from django.conf import settings
from contactus.forms import contactForm
from home.views import home
from store.utils import cookieCart, cartData
from django.core import mail
from django.utils.html import strip_tags

# Views for the contact us app.

def contact(request):
    if request.method == 'GET':
        form = contactForm()
        data = cartData(request)
        cartItems = data['cartItems']
        
        context = {'form' : form, 'cartItems': cartItems}
	    
    else:
        """When a user submits the form it starts here. """
        form = contactForm(request.POST)
        
        if form.is_valid():
            from_email = form.cleaned_data['from_email']
            from_name = form.cleaned_data['from_name']
            subject = form.cleaned_data['subject']

            try:
                """Once the forms been validated it then is processed to be send using the credentials in the settings.py file. """
                send_to = settings.DEFAULT_SEND_TO
                message = "Name: {0} \nEmail: {1} \n\nMessage: {2}".format(from_name, from_email, form.cleaned_data['message'])
                
                send_mail(subject, message, from_email, [send_to], from_name)
                
                messages.success(request, "Your email has been sent, we'll get back to you soon as possible.")
                return redirect (home)
                
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect (contact)
        else:
            messages.error(request, "There was a problem with your e-mail address, please double check it's correct.")
            return render(request, 'contact.html', {'form' : form})
    return render(request, "contact.html", context)
    

#  This is the email with details that are sent when the employer hits the 'Post' button on the orders page
#  to notify the customer that the order has been dispatched, and they have a record of the order.
def order_posted_email(order, request):
    
    emailSubject = "Your order {0} from TheScentSqueen has been dispatched.".format(order.order.transaction_id)
    emailOfSender = settings.DEFAULT_SEND_TO
    emailOfRecipient = '{0}'.format(order.email_address)

    context = ({'order':order}) 
    
    text_content = render_to_string('receipt_email.txt', context, request=request)
    html_content = render_to_string('receipt_email.html', context, request=request)

    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject=emailSubject, body=text_content, from_email=emailOfSender, to=[emailOfRecipient,], reply_to=[emailOfSender,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)

    except:
        print('There was an error sending an email') 
