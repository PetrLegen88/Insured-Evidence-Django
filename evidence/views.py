from django.shortcuts import render, redirect
from .models import Insured, Insurance, InsuranceEvent




def homepage(request):
    return render(request, 'homepage.html')


def insured(request):
    insureds = Insured.objects.all()
    return render(request, 'insured.html', {'insureds': insureds})





