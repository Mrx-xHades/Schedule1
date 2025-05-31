from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True)
    email = models.EmailField(unique=True)

    is_client = models.BooleanField(default=False)
    is_barber = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)  # 👈 Adicione isso


    USERNAME_FIELD = 'email'  # login será feito via email
    REQUIRED_FIELDS = ['username']  # campos obrigatórios além do email

    def __str__(self):
        return self.first_name or self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.email
