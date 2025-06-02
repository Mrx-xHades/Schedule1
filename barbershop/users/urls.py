from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailLoginForm  # importa o form de login via e-mail
from django.views.generic import TemplateView 

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html',  # use o caminho correto do template
            authentication_form=EmailLoginForm
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrar/', views.register, name='register'),
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
]
