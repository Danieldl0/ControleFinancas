from django.forms import ModelForm, CharField, EmailField, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserForm(ModelForm):
    # modificando os parametros dos atributos da classe User
    username = CharField(help_text=None, label="Usuario")
    first_name = CharField(required=True, label="Nome")
    last_name = CharField(required=True, label="Sobrenome")
    email = EmailField(required=True)
    password = CharField(required=True, widget=PasswordInput(), validators=[validate_password], label="Senha")
    password2 = CharField(required=True, widget=PasswordInput(), label="Confirmar senha")

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password"]


    ''' sobrepondo metodo clean para validar 
        que a senha é a confirmar senha dela são iguais. '''
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        
        if password != password2:
            self.add_error("password2", "As senhas devem ser iguais")
        
        return cleaned_data

    # funcao para colocar o atributo class = "form-control" do boostrap em todos os campos do fomulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'