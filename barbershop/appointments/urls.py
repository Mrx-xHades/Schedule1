from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.list_appointments, name='list'),
    path('agendar/', views.schedule_appointment, name='schedule'),
    path('horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('editar/<int:pk>/', views.editar_agendamento, name='editar_agendamento'),
    path('cancelar/<int:pk>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('historico/', views.historico_agendamentos, name='historico'),
    path('admin/agendamentos/', views.list_all, name='list_all'),
    path('barber/agendamento/<int:pk>/confirmar/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('barber/agendamento/<int:pk>/concluido/', views.concluido, name='concluido'),
]
