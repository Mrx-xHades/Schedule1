from django import forms
from django.contrib.auth import get_user_model
from .models import Appointment
from django.forms import DateInput, Select
from django.core.exceptions import ValidationError
from datetime import date

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'barber', 'date', 'time']
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()
        self.fields['barber'].queryset = User.objects.filter(is_barber=True)
        self.fields['time'].choices = []  # Preenchido via JavaScript

    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        if selected_date and selected_date < date.today():
            raise ValidationError("Você não pode agendar para uma data que já passou.")
        return selected_date

    def clean(self):
        cleaned_data = super().clean()
        barber = cleaned_data.get('barber')
        date_ = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if barber and date_ and time:
            conflitos = Appointment.objects.filter(
                barber=barber,
                date=date_,
                time=time
            ).exclude(status='cancelado')

            # Se for edição, exclui o próprio agendamento da checagem
            if self.instance.pk:
                conflitos = conflitos.exclude(pk=self.instance.pk)

            if conflitos.exists():
                raise ValidationError("Já existe um agendamento ativo nesse horário com esse barbeiro.")

        return cleaned_data
