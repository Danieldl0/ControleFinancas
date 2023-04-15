from django.forms import ModelForm, DateInput
from .models import Receita, Despesa


class ReceitaForm(ModelForm):
    class Meta:
        model = Receita # entidade utilizada para criação do formulario
        fields = '__all__' # campos que serao utilizados no formulario
        widgets = { 
            'data': DateInput(attrs={'type': 'date',}), #transformando o campo data no tipo date
        }

    # funcao para colocar o atributo class = "form-control" do boostrap em todos os campos do fomulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

  
class DespesaForm(ModelForm):
    class Meta:
        model = Despesa # entidade utilizada para criação do formulario
        fields = '__all__' # campos que serao utilizados no formulario
        widgets = { 
            'data': DateInput(attrs={'type': 'date',}), #transformando o campo data no tipo date
        }

    # funcao para colocar o atributo class = "form-control" do boostrap em todos os campos do fomulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'