from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.list_appointments, name='list'),  # /agendamentos/
    path('agendar/', views.schedule_appointment, name='schedule'),  # /agendamentos/agendar/
    path('horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),  # <-- ESSA É A URL DO AJAX
]
