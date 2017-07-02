from django import forms
from .models import *

class JoinForm(forms.ModelForm):
    class Meta:
        model = Join
        fields ='__all__'

