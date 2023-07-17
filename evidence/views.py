from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InsuredForm, InsuranceForm, InsuranceEventForm, NewInsuranceForm
from .models import Insured, Insurance, InsuranceEvent, RoleEnum
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator


def homepage(request):
    return render(request, 'homepage.html')


def insured(request):
    insured_list = Insured.objects.prefetch_related('insurance')
    paginator = Paginator(insured_list, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'insured.html', {'page_obj': page_obj})


def new_insured(request):
    if request.method == 'POST':
        form = InsuredForm(request.POST)
        if form.is_valid():
            insured = form.save(commit=False)
            if insured.role == RoleEnum.INSURER.value:
                insured.is_policyholder = True
            insured.save()
            messages.success(request, 'The insured has been saved.')
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
    insurance_objects = Insurance.objects.all()
    for insurance in insurance_objects:
        insured_names = [f"{insured.first_name} {insured.last_name}" for insured in insurance.insurance.all()]
        insurance.insured_names = ", ".join(insured_names)
    paginator = Paginator(insurance_objects, 7)
    page_number = request.GET.get('page')
    insurances = paginator.get_page(page_number)
    return render(request, 'insurances.html', {'insurances': insurances, 'page_obj': insurances})


@login_required
def new_insurance(request):
    if request.method == 'POST':
        form = NewInsuranceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insurances')  # Přesměrování na seznam pojištění po úspěšném vytvoření
    else:
        form = NewInsuranceForm()

    context = {
        'form': form,
        'insured': Insured.objects.all(),
    }
    return render(request, 'new_insurance.html', context)


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

    return render(request, 'edit_insured.html', {'form': form, 'insured': insured})


def delete_insurance(request, insurance_id):
    insurance = Insurance.objects.get(pk=insurance_id)
    insured_id = insurance.insurance.first().id
    insurance.delete()
    return redirect('insured_detail', insured_id=insured_id)


def edit_insurance(request, insurance_id):
    insurance = get_object_or_404(Insurance, id=insurance_id)
    insured = insurance.insurance.first()

    if request.method == 'POST':
        form = InsuranceForm(request.POST, instance=insurance)
        if form.is_valid():
            form.save()
            return redirect('insured_detail', insured_id=insurance.insurance.first().id)
    else:
        form = InsuranceForm(instance=insurance)

    context = {
        'form': form,
        'insurance': insurance,
        'insured': insured,

    }
    return render(request, 'edit_insurance.html', context)


def insurance_events(request):
    events = InsuranceEvent.objects.all()
    for event in events:
        insured_names = ", ".join([insured.first_name for insured in event.insurance.insurance.all()])
        setattr(event, 'insured_names', insured_names)

    events = InsuranceEvent.objects.order_by('id')
    paginator = Paginator(events, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'insurance_events.html', {'page_obj': page_obj})


def insurance_event_detail(request, event_id):
    event = InsuranceEvent.objects.get(id=event_id)
    insured_names = ", ".join([insured.first_name for insured in event.insurance.insurance.all()])
    context = {
        'event': event,
        'insured_names': insured_names
    }
    return render(request, 'insurance_event_detail.html', context)


def delete_event(request, event_id):
    event = InsuranceEvent.objects.get(id=event_id)

    if request.method == 'POST':
        event.delete()
        return redirect('insurance_events')

    context = {
        'event': event
    }
    return render(request, 'delete_event.html', context)


def create_event(request):
    if request.method == 'POST':
        form = InsuranceEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insurance_events')
    else:
        form = InsuranceEventForm()

    context = {
        'form': form
    }
    return render(request, 'create_event.html', context)


def edit_event(request, event_id):
    event = get_object_or_404(InsuranceEvent, id=event_id)
    if request.method == 'POST':
        form = InsuranceEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('insurance_event_detail', event_id=event_id)
    else:
        form = InsuranceEventForm(instance=event)
    context = {
        'form': form,
        'event': event
    }
    return render(request, 'edit_event.html', context)
