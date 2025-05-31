from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # substitui RedirectView por TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('usuarios/', include('barbershop.users.urls')),
    path('agendamentos/', include('barbershop.appointments.urls')),
    path('dashboard/', include('barbershop.dashboard.urls')),

    # Página inicial: landing page
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
]
