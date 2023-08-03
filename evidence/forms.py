from django import forms
from .models import Insured, Insurance, InsuranceEvent, RoleEnum


class InsuredForm(forms.ModelForm):
    class Meta:
        model = Insured
        fields = ['first_name', 'last_name', 'email', 'phone', 'street', 'city', 'zipcode', 'role']


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['type', 'subject', 'amount', 'valid_from', 'valid_until']


class InsuranceEventForm(forms.ModelForm):
    class Meta:
        model = InsuranceEvent
        fields = ['insurance', 'subject', 'description', 'date_submitted', 'status', 'note']


class NewInsuranceForm(forms.ModelForm):
    insured = forms.ModelChoiceField(queryset=Insured.objects.all(), label='Insured')

    class Meta:
        model = Insurance
        fields = ['insured', 'type', 'subject', 'amount', 'valid_from', 'valid_until']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        instance.insurance.set([self.cleaned_data['insured']])
        if commit:
            instance.save()
        return instance


class PolicyholderForm(forms.Form):
    insured = forms.ModelChoiceField(
        queryset=Insured.objects.filter(role=RoleEnum.Policyholder.value),
        label='Policyholder',
        widget=forms.Select
    )


class CompleteEventForm(forms.ModelForm):
    class Meta:
        model = InsuranceEvent
        fields = '__all__'
