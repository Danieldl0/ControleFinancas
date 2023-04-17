from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReceitaForm, DespesaForm
from django.urls import reverse
from .models import Receita, Despesa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
from django.core.paginator import Paginator
import csv, os
from secrets import token_urlsafe
from django.conf import settings



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

    # pegando o value dos campos dos seus respectivos nomes
    busca = request.GET.get('busca')
    filtro_nome = request.GET.get('filtro_nome')
    filtro_valor = request.GET.get('filtro_valor')
    filtro_categoria = request.GET.get('filtro_categoria')
    filtro_data1 = request.GET.get('filtro_data1')
    filtro_data2 = request.GET.get('filtro_data2')
    exportar_csv = request.GET.get('exportar_csv')

    # checando se apertou o botão de exportar
    if exportar_csv:
        if filtro_data2 < filtro_data1: # verificando se a data final é menor que a data inicio
                messages.add_message(request, constants.ERROR, "A data inicio deve ser menor que a data final")
                return redirect('lista_receita')
        
        try:
            receitas = Receita.objects.filter(
            criador=request.user,
            data__range = (filtro_data1, filtro_data2)
            )
        except: # testando se tem data e está no formato correto
            messages.add_message(request, constants.ERROR, "Selecione um periodo")
            return redirect('lista_receita')

        return gerar_csv(receitas) # retornando o csv para download

    if busca:# checando se apertou o botão de exportar
        if filtro_data1 and filtro_data2:# verificando se possui um periodo de data selecionado
            if filtro_data2 < filtro_data1: # verificando se a data final é menor que a data inicio
                messages.add_message(request, constants.ERROR, "A data inicio deve ser menor que a data final")
                return redirect('lista_receita')
            
            receitas = Receita.objects.filter( # criando um objeto com os filtros possiveis
                criador=request.user,
                nome__icontains=filtro_nome,
                valor__startswith=filtro_valor,
                categoria__icontains=filtro_categoria,
                data__range = (filtro_data1, filtro_data2)
                )
        else:  # caso nao tenha data informada, cria um objeto com filtro sem a data
            receitas = Receita.objects.filter(
                criador=request.user,
                nome__icontains=filtro_nome,
                valor__startswith=filtro_valor,
                categoria__icontains=filtro_categoria
                )

    # adicionando paginação de 10 objetos por pagina 
    paginator = Paginator(receitas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, template_name, {"page_obj": page_obj})


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
        receita.delete() # deletando o objeto do banco de dados
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
            messages.add_message(request, constants.ERROR, 'já existe essa Despesa')
            return redirect(reverse('cadastro_despesa'))

        despesa.save() # salvando uma nova despesa no banco de dados
        messages.add_message(request, constants.SUCCESS, 'Despesa cadastrada com sucesso')
        return redirect(reverse('cadastro_despesa'))
    return render(request, template_name, {"form": form})


# view listar
@login_required
def lista_despesa(request, template_name="despesa/lista_despesa.html"):
    despesas = Despesa.objects.filter(criador=request.user)

    busca = request.GET.get('busca')
    filtro_nome = request.GET.get('filtro_nome')
    filtro_valor = request.GET.get('filtro_valor')
    filtro_categoria = request.GET.get('filtro_categoria')
    filtro_data1 = request.GET.get('filtro_data1')
    filtro_data2 = request.GET.get('filtro_data2')
    exportar_csv = request.GET.get('exportar_csv')

    # checando se apertou o botão de exportar
    if exportar_csv:
        if filtro_data2 < filtro_data1: # verificando se a data final é menor que a data inicio
                messages.add_message(request, constants.ERROR, "A data inicio deve ser menor que a data final")
                return redirect('lista_despesa')
        
        try: # testando se tem data e está no formato correto
            despesas = Despesa.objects.filter(
            criador=request.user,
            data__range = (filtro_data1, filtro_data2)
            )
        except:
            messages.add_message(request, constants.ERROR, "Selecione um periodo")
            return redirect('lista_despesa')

        return gerar_csv(despesas) # retornando o csv para download


    if busca: # checando se apertou o botão de exportar
        if filtro_data1 and filtro_data2: # verificando se possui um periodo de data selecionado
            if filtro_data2 < filtro_data1: # verificando se a data final é menor que a data inicio
                messages.add_message(request, constants.ERROR, "A data inicio deve ser menor que a data final")
                return redirect('lista_receita')

            
            despesas = Despesa.objects.filter( # criando um objeto com os filtros possiveis
                criador=request.user,
                nome__icontains=filtro_nome,
                valor__startswith=filtro_valor,
                categoria__icontains=filtro_categoria,
                data__range = (filtro_data1, filtro_data2)
                )
        else: # caso nao tenha data informada, cria um objeto com filtro sem a data  
            despesas = Despesa.objects.filter(
                criador=request.user,
                nome__icontains=filtro_nome,
                valor__startswith=filtro_valor,
                categoria__icontains=filtro_categoria
                )
        
    # adicionando paginação de 10 objetos por pagina
    paginator = Paginator(despesas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, template_name, {"page_obj": page_obj})



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
        despesa.delete() # deletando o objeto do banco de dados
        return redirect('lista_despesa')
    return render(request, template_name, {"despesa": despesa})



# metodo gerar csv
def gerar_csv(list_obj):
    
    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    with open(path, 'w') as arq:
        writer = csv.writer(arq, delimiter=",")
        for obj in list_obj:
            x = (obj.nome, obj.data, obj.valor, obj.categoria)
            writer.writerow(x)

    return redirect(f'/media/{token}')

        