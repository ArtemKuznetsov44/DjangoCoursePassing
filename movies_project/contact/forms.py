from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Contact


class ContactForm(forms.ModelForm):
    """ Form for email subscription """
    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ['email', 'captcha']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'editContent', 'placeholder': 'Enter your email address...'})

        }
        labels = {
            'email': ''
        }
