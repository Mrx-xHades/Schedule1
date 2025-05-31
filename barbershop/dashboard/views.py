from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from barbershop.users.models import User
from barbershop.appointments.models import Service
from .forms import AdminPasswordResetForm, ServiceForm

# 🔧 Função utilitária para verificar se é admin/barbeiro
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_barber)

# 🔸 Listar usuários cadastrados
@login_required
@user_passes_test(is_admin)
def usuarios_list(request):
    usuarios = User.objects.all().order_by('first_name')
    return render(request, 'dashboard/users_list.html', {'usuarios': usuarios})

# 🔸 Redefinir senha de usuário
@login_required
@user_passes_test(is_admin)
def redefinir_senha(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminPasswordResetForm(request.POST)
        if form.is_valid():
            nova_senha = form.cleaned_data['new_password']
            user.set_password(nova_senha)
            user.must_change_password = True
            user.save()
            messages.success(request, f"A senha de {user.first_name} foi redefinida com sucesso.")
            return redirect('dashboard:usuarios_list')
    else:
        form = AdminPasswordResetForm()

    return render(request, 'dashboard/reset_password.html', {'form': form, 'target_user': user})

# 🔸 Criar novo serviço (barbeiro atribuído automaticamente)
@login_required
@user_passes_test(is_admin)
def criar_servico(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            servico = form.save(commit=False)  # ✅ CORREÇÃO: define 'servico'
            servico.barber = request.user      # ✅ preenche automaticamente
            servico.save()
            messages.success(request, "Serviço cadastrado com sucesso!")
            return redirect('dashboard:usuarios_list')  # ou: dashboard:lista_servicos futuramente
    else:
        form = ServiceForm()

    return render(request, 'dashboard/service_form.html', {'form': form})
