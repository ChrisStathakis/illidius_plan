from django import forms

from .models import GymPerson



class GymPersonForm(forms.ModelForm):

    class Meta:
        model = GymPerson
        fields = '__all__'
        exclude = ['name', 'slugfield']