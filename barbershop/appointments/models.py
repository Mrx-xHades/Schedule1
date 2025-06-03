from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Service(models.Model):
    barber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_barber': True}
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - R${self.price}"


class Appointment(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        limit_choices_to={'is_client': True}
    )
    barber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments_barber',
        limit_choices_to={'is_barber': True}
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    def __str__(self):
        return f"{self.date} às {self.time} com {self.barber}"

    def clean(self):
        conflito = Appointment.objects.filter(
            barber=self.barber,
            date=self.date,
            time=self.time
        ).exclude(status='cancelado')

        # Ignora a si mesmo se estiver editando
        if self.pk:
            conflito = conflito.exclude(pk=self.pk)

        if conflito.exists():
            raise ValidationError("Já existe um agendamento ativo com este barbeiro neste horário.")

    def save(self, *args, **kwargs):
        self.full_clean()  # chama clean() antes de salvar
        super().save(*args, **kwargs)
