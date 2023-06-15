from django.shortcuts import render, redirect
from .forms import RegistrationForm


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = RegistrationForm()
    return render(request, 'sign_up.html', {'form': form})
