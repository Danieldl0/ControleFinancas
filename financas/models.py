from django.db import models
from django.contrib.auth.models import User

# Modelo base para as classes receita e despesa
class Financas(models.Model):
    criador = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=50, blank=False, null=False)
    valor = models.FloatField(blank=False, null=False)
    data = models.DateField(blank=False, null=False)
    descricao = models.TextField(blank=True, null=True)
    comprovante = models.FileField(upload_to="comprovantes", blank=False, null=False)

    def __str__(self):
        return self.nome
    

class Receita(Financas): # Herda de Financas
    OPCOES = (("Investimento","Investimento"),
              ("Presente","Presente"),
              ("Prêmio","Prêmio"),
              ("Salário","Salário"),
              ("Outros","Outros"))
    categoria = models.CharField(max_length=20, choices=OPCOES, blank=False, null=False)

    def __str__(self):
        return self.nome

  
class Despesa(Financas): # Herda de Financas
    OPCOES = (("Casa","Casa"),
              ("Educação","Educação"),
              ("Eletrônicos","Eletrônicos"),
              ("Lazer","Lazer"),
              ("Saúde","Saúde"),
              ("Supermercado","Supermercado"),
              ("Transporte","Transporte"),
              ("Outros","Outros"))
    categoria = models.CharField(max_length=20, choices=OPCOES, blank=False, null=False)

    def __str__(self):
        return self.nome