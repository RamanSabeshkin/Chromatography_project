from django import forms
from . import models
from django.contrib.auth.models import User


class CompoundIDform(forms.Form):
    cid_number = forms.IntegerField()


class CompoundDescriptorform(forms.Form):
    dipole_moment = forms.FloatField()
    electron_excess_charge = forms.FloatField()
    was = forms.FloatField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('bad password')
        return cd['password']



