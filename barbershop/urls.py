from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('usuarios/', include('barbershop.users.urls')),  # login, logout, cadastro
    path('agendamentos/', include('barbershop.appointments.urls')),  # agendar, listar

    # Redireciona / para agendamentos
    path('', RedirectView.as_view(url='/agendamentos/', permanent=False)),
]
