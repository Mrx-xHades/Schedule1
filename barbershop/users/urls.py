from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailLoginForm  # importa o form de login via e-mail
from .views import home


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
    path('', home, name='home'),
    path('carrossel/', views.carousel_list, name='carousel_list'),
    path('carrossel/add/', views.carousel_add, name='carousel_add'),
    path('carrossel/edit/<int:pk>/', views.carousel_edit, name='carousel_edit'),
    path('carrossel/delete/<int:pk>/', views.carousel_delete, name='carousel_delete'),

]
