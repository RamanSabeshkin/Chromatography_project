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

