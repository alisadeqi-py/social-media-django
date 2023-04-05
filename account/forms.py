from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 




class UserRegisterationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    password2 = forms.CharField(label='confirm password')

    def clean_email(self):
        email=self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('thos eamil already exists')
        return email
    
    def clean(self):

        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password most match')
        
        
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
