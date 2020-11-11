from django import forms

# Simple contact form.
class contactForm(forms.Form):
    from_email = forms.EmailField(required=True, label="Your Email:")
    from_name = forms.CharField(required=True, label="Your Name:")
    subject = forms.CharField(required=True, label="Title:")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message:")