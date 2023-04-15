from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="inicio"),
    path('receita/cadastro/', cadastro_receita, name="cadastro_receita"),
    path('despesa/cadastro/', cadastro_despesa, name="cadastro_despesa"),
]
