from django.db import models

# Create your models here.


class Financas(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.FloatField()
    data = models.DateField()
    descricao = models.TextField(blank=True, null=True)
    comprovante = models.FileField(upload_to="comprovantes")

    def __str__(self):
        return self.nome
    

class Receita(Financas):
    OPCOES = (("Inv","Investimento"),
              ("Pst","Presente"),
              ("Prm","Prêmio"),
              ("Slr","Salário"),
              ("O","Outros"))
    categoria = models.CharField(max_length=20, choices=OPCOES)

    def __str__(self):
        return self.nome
    
class Despesa(Financas):
    OPCOES = (("Csa","Casa"),
              ("Edu","Educação"),
              ("Elt","Eletrônicos"),
              ("lzr","Lazer"),
              ("Sau","Saúde"),
              ("Sup","Supermercado"),
              ("Tpt","Transporte"),
              ("O","Outros"))
    categoria = models.CharField(max_length=20, choices=OPCOES)

    def __str__(self):
        return self.nome