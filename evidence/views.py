from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InsuredForm, InsuranceForm, InsuranceEventForm, NewInsuranceForm, PolicyholderForm
from .models import Insured, Insurance, InsuranceEvent, RoleEnum
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator


def homepage(request):
    return render(request, 'homepage.html')


def insured(request):
    filter_by = request.GET.get('filter_by')
    keyword = request.GET.get('keyword')

    insured_list = Insured.objects.prefetch_related('insurance')

    if filter_by == 'name':
        insured_list = insured_list.filter(first_name__icontains=keyword) | insured_list.filter(last_name__icontains=keyword)
    elif filter_by == 'city':
        insured_list = insured_list.filter(city__icontains=keyword)
    elif filter_by == 'street':
        insured_list = insured_list.filter(street__icontains=keyword)
    elif filter_by == 'role':
        insured_list = insured_list.filter(role__icontains=keyword)

    paginator = Paginator(insured_list, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'insured.html', context)


def new_insured(request):
    if request.method == 'POST':
        form = InsuredForm(request.POST)
        if form.is_valid():
            insured = form.save(commit=False)
            if insured.role == RoleEnum.Policyholder.value:
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
    filter_by = request.GET.get('filter_by')
    keyword = request.GET.get('keyword')

    insurance_objects = Insurance.objects.all()

    if filter_by and keyword:
        if filter_by == 'insurance':
            insurance_objects = insurance_objects.filter(type__icontains=keyword)
        elif filter_by == 'insured_name':
            insurance_objects = insurance_objects.filter(insurance__first_name__icontains=keyword) | \
                                insurance_objects.filter(insurance__last_name__icontains=keyword)
        elif filter_by == 'subject':
            insurance_objects = insurance_objects.filter(subject__icontains=keyword)
        elif filter_by == 'amount':
            try:
                keyword = Decimal(keyword)
                insurance_objects = insurance_objects.filter(amount__gt=keyword)
            except (ValueError, TypeError, InvalidOperation):
                messages.error(request, 'You have to enter number.')

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
            return redirect('insurances')
    else:
        form = NewInsuranceForm()

    context = {
        'form': form,
        'insured': Insured.objects.all(),
    }
    return render(request, 'new_insurance.html', context)


def add_policyholder(request, insurance_id):
    insurance = get_object_or_404(Insurance, id=insurance_id)

    if request.method == 'POST':
        form = PolicyholderForm(request.POST)
        if form.is_valid():
            policyholder = form.cleaned_data['insured']
            insurance.insurance.add(policyholder)
            return redirect('insurance_detail', insurance_id=insurance.id)
    else:
        form = PolicyholderForm()

    context = {
        'form': form,
        'insurance': insurance,
    }
    return render(request, 'add_policyholder.html', context)


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
    filter_by = request.GET.get('filter_by')
    keyword = request.GET.get('keyword')

    events = InsuranceEvent.objects.all()
    for event in events:
        insured_names = ", ".join([insured.first_name for insured in event.insurance.insurance.all()])
        setattr(event, 'insured_names', insured_names)

    if filter_by and keyword:
        if filter_by == 'event_id':
            events = events.filter(id__icontains=keyword)
        elif filter_by == 'insurance':
            events = events.filter(insurance__type__icontains=keyword)
        elif filter_by == 'insured':
            events = events.filter(insurance__insurance__first_name__icontains=keyword) | \
                     events.filter(insurance__insurance__last_name__icontains=keyword)
        elif filter_by == 'subject':
            events = events.filter(subject__icontains=keyword)
        elif filter_by == 'status':
            events = events.filter(status__icontains=keyword)

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