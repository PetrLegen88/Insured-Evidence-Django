from django import forms
from .models import Insured


class InsuredForm(forms.ModelForm):
    class Meta:
        model = Insured
        fields = ['first_name', 'last_name', 'email', 'phone', 'street', 'city', 'zipcode']