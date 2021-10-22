from django import forms
from . import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from Chromatography.models import Column


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


class ColumnForm(ModelForm):
    class Meta:
        model = models.Column
        fields = ('type',
                  'name',
                  'abbreviation',
                  'manufacturer',
                  'dimensions',
                  'particle_size',
                  'pore_size',
                  'pore_volume',
                  'surface_area',
                  'carbon_loading',
                  'surface_coverage',
                  'bulk_density',
                  'end_capping',
                  'silica')

class LogPModelForm(ModelForm):
    class Meta:
        model = models.LogPModel