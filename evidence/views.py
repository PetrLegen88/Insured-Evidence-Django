from django.shortcuts import render, redirect, get_object_or_404
from .forms import InsuredForm, InsuranceForm
from .models import Insured
from django.contrib import messages


def homepage(request):
    return render(request, 'homepage.html')


def insured(request):
    insureds = Insured.objects.prefetch_related('insurance')
    return render(request, 'insured.html', {'insureds': insureds})


def new_insured(request):
    if request.method == 'POST':
        form = InsuredForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Pojištěnec byl uložen.')
            form.save()
            return redirect('insured')
    else:
        form = InsuredForm()
    return render(request, 'new_insured.html', {'form': form})


def insured_detail(request, insured_id):
    insured = get_object_or_404(Insured, pk=insured_id)
    return render(request, 'insured_detail.html', {'insured': insured})


def add_insurance(request):
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.insurance_id = request.user.insured.id
            insurance.save()
            return redirect('insured_detail', insured_id=insurance.insurance_id)
    else:
        form = InsuranceForm()
    return render(request, 'add_insurance.html', {'form': form})