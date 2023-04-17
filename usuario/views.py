from django.shortcuts import render, redirect
from .forms import UserForm
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import constants



def login(request, template_name="login.html"):

    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "GET":
        return render(request, template_name)
    if request.method == "POST":
        
        # pegando os dados do fomurlario. username e senha
        username = request.POST.get('username')
        password = request.POST.get('password')

        # autenticando o usuario com os dados de login
        user = auth.authenticate(username=username, password=password)

        # verificando se existe o usuario, caso não retorna uma mensagem de erro
        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect(reverse('login'))

        # Logar o usuario. criando uma seção para o userio autenticado.
        auth.login(request, user)
        return render(request, 'index.html')


def logout(request):
    # encerrando a seção do usuario logado
    auth.logout(request)
    return redirect(reverse('login'))


def cadastro(request, template_name="cadastro.html"):
    #criando uma instancia de UserForm
    form = UserForm(request.POST or None)
    

    #verificando se os dados são validos
    if form.is_valid():
        # criando um novo usuario com os dados do formulario
        user = form.save()
        user.set_password(user.password) # salvando a senha como hash no banco de dados
        user.save()
        return redirect(reverse('login'))
    return render(request, template_name, {"form": form})