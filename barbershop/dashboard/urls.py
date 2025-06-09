from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('usuarios/<int:user_id>/redefinir-senha/', views.redefinir_senha, name='redefinir_senha'),
     # ✅ Nova URL para criar serviço
    path('servicos/novo/', views.criar_servico, name='create_service'),
    path('servicos/', views.lista_servicos, name='lista_servicos'),
    path('servicos/<int:pk>/editar/', views.editar_servico, name='editar_servico'),
    path('servicos/<int:pk>/excluir/', views.excluir_servico, name='excluir_servico'),
    path('reset', views.usuarios_list, name='reset'),
]
