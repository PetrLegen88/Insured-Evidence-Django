from django.shortcuts import render, redirect
from .forms import InsuredForm
from .models import Insured
from django.contrib import messages




def homepage(request):
    return render(request, 'homepage.html')


def insured(request):
    insureds = Insured.objects.all()
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





