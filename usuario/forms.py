from django.forms import ModelForm, CharField, EmailField, ValidationError, PasswordInput
from django.contrib.auth.models import User


class UserForm(ModelForm):
    # modificando os parametros dos atributos da classe User
    username = CharField(help_text=None, label="Usuario")
    first_name = CharField(required=True, label="Nome")
    last_name = CharField(required=True, label="Sobrenome")
    email = EmailField(required=True)
    password2 = CharField(max_length=128, required=True, widget=PasswordInput(), label="Confirmar senha")

    
    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password"]


    ''' sobrepondo metodo clean para validar 
        que a senha é a confirmar senha dela são iguais. '''
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        
        if password != password2:
            raise ValidationError(
                "As senhas devem ser iguais"
            )
        

    # funcao para colocar o atributo class = "form-control" do boostrap em todos os campos do fomulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'