from django.shortcuts import render, redirect
from .forms import ReceitaForm, DespesaForm
from django.urls import reverse
from .models import Receita
from django.contrib.auth.decorators import login_required



def index(request):
    if request.method == "GET":
        return render(request, 'index.html')

#CRUD Receita
#view de cadastro das novas receitas
@login_required
def cadastro_receita(request, template_name='receita/cadastro_receita.html'):
    # criando um objeto da classe ReceitaForm com os dados do formulario
    form = ReceitaForm(request.POST or None, request.FILES or None)

    # verificando se os dados são validos e salvando no banco de dados
    if form.is_valid(): 
        form.save()
        return redirect(reverse('cadastro_receita'))
    return render(request, template_name, {"form": form})


@login_required
def lista_receita(request, template_name="receita/lista_receita.html"):
    receitas = Receita.objects.all()
    return render(request, template_name, {"receitas": receitas})





        
#CRUD Despesa
#view de cadastro das novas despesa
def cadastro_despesa(request, template_name='despesa/cadastro_despesa.html'):
    # criando um objeto da classe DespesaForm com os dados do formulario
    form = DespesaForm(request.POST or None, request.FILES or None)

    # verificando se os dados são validos e salvando no banco de dados
    if form.is_valid(): 
        form.save()
        return redirect(reverse('cadastro_despesa'))
    return render(request, template_name, {"form": form})