from django import forms

from .models import *

class ShortURLForm(forms.Form):
    url = forms.URLField(label='', required=True,)
    costumer_code = forms.CharField(label='', required=False)


