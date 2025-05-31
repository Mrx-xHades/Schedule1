from django import forms
from barbershop.appointments.models import Service
from barbershop.users.models import User

class AdminPasswordResetForm(forms.Form):
    new_password = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite a nova senha'})
    )

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Nome do Serviço"
        self.fields['price'].label = "Preço (R$)"
