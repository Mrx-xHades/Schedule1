from django.contrib.auth import get_user_model
from django.db import models
from barbershop.users.models import User
from django.conf import settings
from datetime import timedelta

class Service(models.Model):
    barber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_barber': True})
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - R${self.price}"

class Appointment(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments', limit_choices_to={'is_client': True})
    barber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_barber', limit_choices_to={'is_barber': True})
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()   
    time = models.TimeField()

    class Meta:
        unique_together = ('barber', 'date', 'time')  # Garante que não haja conflito de horário

    def __str__(self):
        return f"{self.date} às {self.time} com {self.barber}"
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
