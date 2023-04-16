from django.forms import ModelForm, CharField, EmailField, ValidationError, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserForm(ModelForm):
    username = CharField(help_text=None)
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = EmailField(required=True)
    password = CharField(required = True, widget=PasswordInput(), validators=[validate_password])
    password2 = CharField(max_length=128, required=True, label="Confirmar senha", widget=PasswordInput())

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password"]


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError(
                "As senhas devem ser iguais"
            )