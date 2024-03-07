from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from . import models


class AddReviewForm(forms.ModelForm):
    """ Form to add review """

    # Add a field for our form - recaptcha field:
    captcha = ReCaptchaField()

    class Meta:
        model = models.Reviews
        fields = ['text', 'name', 'email', 'captcha']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border'}),
            'text': forms.Textarea(attrs={'class': 'form-control border'})
        }


class RatingForm(forms.ModelForm):
    """ Form to add rating start for movie """

    # We use the ModelChoiceField to use all existing Rating object/values in our db with widget - RadioSelect:
    star = forms.ModelChoiceField(queryset=models.RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = models.Rating
        fields = ('star',)
