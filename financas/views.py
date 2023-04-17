from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReceitaForm, DespesaForm
from django.urls import reverse
from .models import Receita, Despesa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
from datetime import datetime


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

    busca = request.GET.get('busca')
    filtro_nome = request.GET.get('filtro_nome')
    filtro_valor = request.GET.get('filtro_valor')
    filtro_categoria = request.GET.get('filtro_categoria')
    filtro_data1 = request.GET.get('filtro_data1')
    filtro_data2 = request.GET.get('filtro_data2')


    if busca:
        if filtro_data1 and filtro_data2:
            if filtro_data2 < filtro_data1:
                messages.add_message(request, constants.ERROR, "A data inicio deve ser menor que a data final")
                return redirect('lista_receita')

            
            receitas = Receita.objects.filter(
                criador=request.user,
                nome__icontains=filtro_nome,
                valor__startswith=filtro_valor,
                categoria__icontains=filtro_categoria,
                data__range = (filtro_data1, filtro_data2)
                )
        else:   
            receitas = Receita.objects.filter(
                criador=request.user,
                nome__icontains=filtro_nome,
                valor__startswith=filtro_valor,
                categoria__icontains=filtro_categoria
                )

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
@login_required
def cadastro_despesa(request, template_name='despesa/cadastro_despesa.html'):
    # criando um objeto da classe DespesaForm com os dados do formulario
    form = DespesaForm(request.POST or None, request.FILES or None)

    # verificando se os dados são validos e salvando no banco de dados
    if form.is_valid(): 
        despesa = form.save(commit=False)
        despesa.criador = request.user

        #verificando se já existe uma despesa com os mesmo dados
        if Despesa.objects.filter(
            criador = despesa.criador,
            nome = despesa.nome,
            valor = despesa.valor,
            categoria = despesa.categoria,
            data = despesa.data
        ).exists():
            messages.add_message(request, constants.ERROR, 'já existe essa despesa')
            return redirect(reverse('cadastro_despesa'))

        despesa.save() # salvando uma nova despesa no banco de dados
        messages.add_message(request, constants.SUCCESS, 'despesa cadastrada com sucesso')
        return redirect(reverse('cadastro_despesa'))
    return render(request, template_name, {"form": form})


# view listar
@login_required
def lista_despesa(request, template_name="despesa/lista_despesa.html"):
    despesas = Despesa.objects.filter(criador=request.user)

    busca = request.GET.get('busca')
    filtro = request.GET.get('filtro')

    '''
        filtros
        1 = nome
        2 = valor
        3 = data
        4 = categoria
    '''
    if busca:
        if filtro == '1':
            despesas = Despesa.objects.filter(criador=request.user, nome__icontains=busca)

        elif filtro == '2':
            busca = str(despesas.valor).replace(',','.')  # convertendo o valor do html para o formato que está no banco de dados
            despesas = Despesa.objects.filter(criador=request.user, valor__icontains=busca)

        elif filtro == '3':
            try: # convertendo a data do html para o formato que está no banco de dados
                busca = datetime.strptime(str(busca), "%d/%m/%Y").strftime("%Y-%m-%d")
            except:
                messages.add_message(request, constants.ERROR, "Formato de data invalido! Ex: 28/10/1997 ")
                return redirect('lista_despesa')
            
            despesas = Despesa.objects.filter(criador=request.user, data__gte=busca)

        elif filtro == '4':
            despesas = Despesa.objects.filter(criador=request.user, categoria__icontains=busca)
        
    
    return render(request, template_name, {"lista": despesas})


# view detalhe
@login_required
def detalhe_despesa(request, id, template_name="despesa/detalhe_despesa.html"):
    # pegando o objecto especifico, do mesmo id 
    despesa = get_object_or_404(Despesa, id=id)

    # verificando se o usuario foi o criador
    if not despesa.criador == request.user:
        raise Http404("Essa despesa não é sua")

    # metodo get apenas para mostrar o formulario com os dados
    if request.method == "GET":
        form = DespesaForm(instance=despesa)
        return render(request, template_name, {"form": form})
    
    # metodo post recebendo os dados e salvando os dados alterados 
    if request.method == "POST":
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            despesa = form.save()
            messages.add_message(request, constants.SUCCESS, 'Despesa alterada com sucesso')
        return render(request, template_name, {"form": form})


# view deletar 
@login_required
def deleta_despesa(request, id, template_name="despesa/deleta_despesa.html"):
    despesa = get_object_or_404(Despesa, id=id)
    if request.method == "POST":
        despesa.delete()
        return redirect('lista_despesa')
    return render(request, template_name, {"despesa": despesa})

        