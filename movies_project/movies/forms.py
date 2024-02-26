from django import forms
from . import models


class AddReviewForm(forms.ModelForm):
    """ Form to add review """

    class Meta:
        model = models.Reviews
        fields = ['text', 'name', 'email']


class RatingForm(forms.ModelForm):
    """ Form to add rating start for movie """

    # We use the ModelChoiceField to use all existing Rating object/values in our db with widget - RadioSelect:
    star = forms.ModelChoiceField(queryset=models.RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = models.Rating
        fields = ('star',)
