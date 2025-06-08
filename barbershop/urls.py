from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # substitui RedirectView por TemplateView
from django.conf.urls.static import static
from django.conf import settings
from barbershop.users.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('usuarios/', include('barbershop.users.urls')),
    path('agendamentos/', include('barbershop.appointments.urls'), name='agendamentos'),
    path('dashboard/', include('barbershop.dashboard.urls')),

    # Página inicial: landing page
    path('', home, name='home'),
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
