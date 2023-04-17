from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="inicio"),
    
    #urls da receita
    path('receita/cadastro/', cadastro_receita, name="cadastro_receita"),
    path('receita/', lista_receita, name="lista_receita"),
    path('receita/<int:id>/', detalhe_receita, name="datalhe_receita"),
    path('receita/<int:id>/deletar', deleta_receita, name="deleta_receita"),

    #urls da despesa
    path('despesa/cadastro/', cadastro_despesa, name="cadastro_despesa"),
    path('despesa/', lista_despesa, name="lista_despesa"),
    path('despesa/<int:id>/', detalhe_despesa, name="detalhe_despesa"),
    path('despesa/<int:id>/deletar', deleta_despesa, name="deleta_despesa"),
]
