from django.forms import ModelForm, CharField
from django.contrib.auth.models import User

class UserForm(ModelForm):
    username = CharField(help_text=None)
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = CharField(required=True)
    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password"]
        
        