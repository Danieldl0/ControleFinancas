from django.db import models

# Modelo base para as classes receita e despesa
class Financas(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    valor = models.FloatField(blank=False, null=False)
    data = models.DateField(blank=False, null=False)
    descricao = models.TextField(blank=True, null=True)
    comprovante = models.FileField(upload_to="comprovantes", blank=False, null=False)

    def __str__(self):
        return self.nome
    

class Receita(Financas): # Herda de Financas
    OPCOES = (("1","Investimento"),
              ("2","Presente"),
              ("3","Prêmio"),
              ("4","Salário"),
              ("5","Outros"))
    categoria = models.CharField(max_length=20, choices=OPCOES, blank=False, null=False)

    def __str__(self):
        return self.nome

  
class Despesa(Financas): # Herda de Financas
    OPCOES = (("1","Casa"),
              ("2","Educação"),
              ("3","Eletrônicos"),
              ("4","Lazer"),
              ("5","Saúde"),
              ("6","Supermercado"),
              ("7","Transporte"),
              ("8","Outros"))
    categoria = models.CharField(max_length=20, choices=OPCOES, blank=False, null=False)

    def __str__(self):
        return self.nome