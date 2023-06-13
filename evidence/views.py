from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage.html')


def insured(request):
    return render(request, 'insured.html')