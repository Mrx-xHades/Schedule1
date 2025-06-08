from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from barbershop.users.models import User
from .models import CarouselImage


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Labels personalizados
        self.fields['first_name'].label = "Nome completo"
        self.fields['username'].label = "Nome de usuário (opcional)"
        self.fields['email'].label = "E-mail"
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirmação da senha"

        # Campos opcionais e placeholders
        self.fields['username'].required = False
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ex: João da Silva'
        self.fields['username'].widget.attrs['placeholder'] = 'Opcional'
        self.fields['email'].widget.attrs['placeholder'] = 'exemplo@email.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'Digite sua senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower() if email else email


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'Digite seu e-mail'
        })
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            email = email.lower()
            self.cleaned_data['username'] = email

            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Esta conta está inativa.", code='inactive')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True  # Define o campo is_client como True por padrão
        if commit:
            user.save()
        return user
    
class CarouselImageForm(forms.ModelForm):
    class Meta:
        model = CarouselImage
        fields = ['image', 'caption']