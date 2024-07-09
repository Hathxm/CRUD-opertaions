from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class updateform(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("username","password","email","first_name","last_name","date_joined")


