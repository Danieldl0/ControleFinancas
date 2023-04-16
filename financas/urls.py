from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="inicio"),
    
    #urls da receita
    path('receita/cadastro/', cadastro_receita, name="cadastro_receita"),
    path('receita/', lista_receita, name="lista_receita"),

    #urls da despesa
    path('despesa/cadastro/', cadastro_despesa, name="cadastro_despesa"),
]
