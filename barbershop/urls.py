from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # substitui RedirectView por TemplateView
from django.conf.urls.static import static
from django.conf import settings
from barbershop.users.views import home
from barbershop.users import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('usuarios/', include('barbershop.users.urls')),
    path('agendamentos/', include('barbershop.appointments.urls'), name='agendamentos'),
    path('dashboard/', include('barbershop.dashboard.urls')),
    path('', home, name='home'),
    path('carrossel/', views.carousel_list, name='carousel_list'),
    path('carrossel/add/', views.carousel_add, name='carousel_add'),
    path('carrossel/edit/<int:pk>/', views.carousel_edit, name='carousel_edit'),
    path('carrossel/delete/<int:pk>/', views.carousel_delete, name='carousel_delete'),
]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
