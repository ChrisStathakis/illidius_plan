from django import forms
from .models import *
import mailchimp
from django.conf import settings

class JoinForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Γράψτε το email σας',
                                                            })
                             )

    class Meta:
        model = Join
        fields = ['email']

    def clean(self):
        email = self.cleaned_data.get('email')
        qs = Join.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Έχετε χρησιμοποιήσει ήδη αυτό το Email')
        print('here')
        API_KEY = settings.MAILCHIMP_API_KEY
        LIST_ID = settings.MAILCHIMP_SUBSCRIBE_LIST_ID
        api = mailchimp.Mailchimp(API_KEY)
        api.lists.subscribe(LIST_ID, {'email': email})
        print('still')

