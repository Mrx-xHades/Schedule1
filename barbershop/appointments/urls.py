from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.list_appointments, name='list'),
    path('agendar/', views.schedule_appointment, name='schedule'),
    path('horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('agendamentos/editar/<int:pk>/', views.editar_agendamento, name='editar_agendamento'),
    path('agendamentos/cancelar/<int:pk>/', views.cancelar_agendamento, name='cancelar_agendamento'),  # ✅ Nova rota
    path('historico/', views.historico_agendamentos, name='historico'),
]

