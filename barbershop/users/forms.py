# barbershop/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from barbershop.users.models import User  # Importe seu modelo personalizado

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Ajuste os campos conforme necessário