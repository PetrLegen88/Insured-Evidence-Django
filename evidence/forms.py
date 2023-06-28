from django import forms
from .models import Insured, Insurance, InsuranceEvent


class InsuredForm(forms.ModelForm):
    class Meta:
        model = Insured
        fields = ['first_name', 'last_name', 'email', 'phone', 'street', 'city', 'zipcode']


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['type', 'subject', 'amount', 'valid_from', 'valid_until']


class InsuranceEventForm(forms.ModelForm):
    class Meta:
        model = InsuranceEvent
        fields = ['insurance', 'subject', 'description', 'date', 'status', 'note']
