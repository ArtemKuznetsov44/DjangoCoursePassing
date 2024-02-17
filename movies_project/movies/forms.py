from django import forms
from . import models

class AddReviewForm(forms.ModelForm):
    """ Form to add review """

    class Meta:
        model = models.Reviews
        fields = ['text', 'name', 'email']