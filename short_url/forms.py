from django import forms
from django.core.exceptions import ValidationError
from .models import *

class ShortURLForm(forms.ModelForm):
    url = forms.URLField(label='URL', required=True, widget=forms.URLInput(attrs={'class': 'form-control'}))
    costumer_code = forms.CharField(label='Preferred Code', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ShortingURL
        fields = ['url', 'costumer_code']


    def clean_costumer_code(self):
        data = self.cleaned_data.get('costumer_code')
        if len(data) < 7 and data:
            raise forms.ValidationError('The length of the code must be at least 6 letters.')

