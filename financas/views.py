from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReceitaForm, DespesaForm
from django.urls import reverse
from .models import Receita
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404


@login_required
def index(request):
    if request.method == "GET":
        return render(request, 'index.html')


#CRUD Receita
#view de cadastro
@login_required
def cadastro_receita(request, template_name='receita/cadastro_receita.html'):
    # criando um objeto da classe ReceitaForm com os dados do formulario
    form = ReceitaForm(request.POST or None, request.FILES or None)

    # verificando se os dados são validos e salvando no banco de dados
    if form.is_valid(): 
        receita = form.save(commit=False)
        receita.criador = request.user

        #verificando se já existe uma receita com os mesmo dados
        if Receita.objects.filter(
            criador = receita.criador,
            nome = receita.nome,
            valor = receita.valor,
            categoria = receita.categoria,
            data = receita.data
        ).exists():
            messages.add_message(request, constants.ERROR, 'já existe essa receita')
            return redirect(reverse('cadastro_receita'))

        receita.save() # salvando uma nova receita no banco de dados
        messages.add_message(request, constants.SUCCESS, 'Receita cadastrada com sucesso')
        return redirect(reverse('cadastro_receita'))
    return render(request, template_name, {"form": form})


# view listar
@login_required
def lista_receita(request, template_name="receita/lista_receita.html"):
    receitas = Receita.objects.filter(criador=request.user)
    return render(request, template_name, {"lista": receitas})


# view detalhe
@login_required
def detalhe_receita(request, id, template_name="receita/detalhe_receita.html"):
    # pegando o objecto especifico, do mesmo id 
    receita = get_object_or_404(Receita, id=id)

    # verificando se o usuario foi o criador
    if not receita.criador == request.user:
        raise Http404("Essa receita não é sua")

    # metodo get apenas para mostrar o formulario com os dados
    if request.method == "GET":
        form = ReceitaForm(instance=receita)
        return render(request, template_name, {"form": form})
    
    # metodo post recebendo os dados e salvando os dados alterados 
    if request.method == "POST":
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            receita = form.save()
            messages.add_message(request, constants.SUCCESS, 'Receita alterada com sucesso')
        return render(request, template_name, {"form": form})


# view deletar 
@login_required
def deleta_receita(request, id, template_name="receita/deleta_receita.html"):
    receita = get_object_or_404(Receita, id=id)
    if request.method == "POST":
        receita.delete()
        return redirect('lista_receita')
    return render(request, template_name, {"receita": receita})

        


#CRUD Despesa
#view de cadastro
def cadastro_despesa(request, template_name='despesa/cadastro_despesa.html'):
    # criando um objeto da classe DespesaForm com os dados do formulario
    form = DespesaForm(request.POST or None, request.FILES or None)
    # verificando se os dados são validos e salvando no banco de dados
    if form.is_valid(): 
        form.save()
        return redirect(reverse('cadastro_despesa'))
    
    return render(request, template_name, {"form": form})