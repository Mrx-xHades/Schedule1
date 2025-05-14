from django import forms
from django.contrib.auth import get_user_model
from .models import Appointment
from django.forms import DateInput, Select

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'barber', 'date', 'time']
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': Select(attrs={'class': 'form-control'}),
        }


    def init(self, args, **kwargs):
        super().init(args, **kwargs)
        User = get_user_model()
        # Garante que só barbeiros apareçam na lista de seleção
        self.fields['barber'].queryset = User.objects.filter(is_barber=True)
        self.fields['time'].choices = []  # Preenchido via JavaScript