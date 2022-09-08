from django import forms
from .models import Profile, phone_regex
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Data
from dataclasses import fields

def email_exist(value):
    if User.objects.filter(email=value).exists():
        return forms.ValidationError("Profile with this Email Address already exists")

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[email_exist])
    class Meta:
        model = User
        fields  =['username','email']

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=17,validators=[phone_regex])
    
    class Meta:
        model = Profile
        fields = ['phone_number']

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['client_name', 'gender', 'mstatus',  'dependance',  'education', 'self_employed', 'appIncome', 'co_appIncome', 'loan_amount', 'loan_amount_term', 'credit_history', 'property_area']