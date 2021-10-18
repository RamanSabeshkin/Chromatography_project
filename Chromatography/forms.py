from django import forms
from . import models


class CompoundIDform(forms.Form):
    cid_number = forms.IntegerField()

