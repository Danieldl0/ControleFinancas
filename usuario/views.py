from django.shortcuts import render, redirect
from .forms import UserForm
from django.urls import reverse

# Create your views here.

def login(request, template_name="login.html"):

    return render(request, template_name)


def cadastro(request, template_name="cadastro.html"):
    form = UserForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(reverse('login'))
    return render(request, template_name, {"form": form})