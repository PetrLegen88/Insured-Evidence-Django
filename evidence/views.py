from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InsuredForm, InsuranceForm
from .models import Insured, Insurance
from django.contrib import messages
from django.urls import reverse


def homepage(request):
    return render(request, 'homepage.html')


def insured(request):
    insureds = Insured.objects.prefetch_related('insurance')
    return render(request, 'insured.html', {'insureds': insureds})


def new_insured(request):
    if request.method == 'POST':
        form = InsuredForm(request.POST)
        if form.is_valid():
            messages.success(request, 'The insured has been saved.')
            form.save()
            return redirect('insured')
    else:
        form = InsuredForm()
    return render(request, 'new_insured.html', {'form': form})


def insured_detail(request, insured_id):
    insured = get_object_or_404(Insured, pk=insured_id)
    return render(request, 'insured_detail.html', {'insured': insured, 'insured_id': insured_id})


@login_required
def add_insurance(request, insured_id):
    insured = get_object_or_404(Insured, pk=insured_id)
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.save()
            insured.insurance.add(insurance)
            return redirect(reverse('insured_detail', args=[insured.id]))
    else:
        form = InsuranceForm()
    return render(request, 'add_insurance.html', {'form': form, 'insured': insured})


def insurances(request):
    insurances = Insurance.objects.all()
    for insurance in insurances:
        insured_names = [f"{insured.first_name} {insured.last_name}" for insured in insurance.insurance.all()]
        insurance.insured_names = ", ".join(insured_names)
    return render(request, 'insurances.html', {'insurances': insurances})


def insurance_detail(request, insurance_id):
    insurance = Insurance.objects.get(id=insurance_id)
    insured_names = [f"{insured.first_name} {insured.last_name}" for insured in insurance.insurance.all()]
    insurance.insured_names = ", ".join(insured_names)
    return render(request, 'insurance_detail.html', {'insurance': insurance})


def delete_insured(request, insured_id):
    insured = get_object_or_404(Insured, pk=insured_id)

    policies = Insurance.objects.filter(insurance=insured)
    policies.delete()

    insured.delete()
    messages.success(request, 'The insured has been deleted.')
    return redirect('insured')


def edit_insured(request, insured_id):
    insured = get_object_or_404(Insured, id=insured_id)

    if request.method == 'POST':
        form = InsuredForm(request.POST, instance=insured)
        if form.is_valid():
            form.save()
            return redirect('insured')
    else:
        form = InsuredForm(instance=insured)

    return render(request, 'edit_insured.html', {'form': form})
