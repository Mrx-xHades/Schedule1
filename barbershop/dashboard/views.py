from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from barbershop.users.models import User
from barbershop.appointments.models import Service
from .forms import AdminPasswordResetForm, ServiceForm

# 🔧 Verificação se o usuário é admin ou barbeiro
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_barber)

# 📋 Listar usuários cadastrados
@login_required
@user_passes_test(is_admin)
def usuarios_list(request):
    usuarios = User.objects.all().order_by('first_name')
    return render(request, 'dashboard/users_list.html', {'usuarios': usuarios})

# 🔒 Redefinir senha de usuário
@login_required
@user_passes_test(is_admin)
def redefinir_senha(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = AdminPasswordResetForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        nova_senha = form.cleaned_data['new_password']
        user.set_password(nova_senha)
        user.must_change_password = True
        user.save()
        messages.success(request, f"A senha de {user.first_name} foi redefinida com sucesso.")
        return redirect('dashboard:usuarios_list')

    return render(request, 'dashboard/reset_password.html', {'form': form, 'target_user': user})

# ➕ Criar novo serviço
@login_required
@user_passes_test(is_admin)
def criar_servico(request):
    form = ServiceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        servico = form.save(commit=False)
        servico.barber = request.user
        servico.save()
        messages.success(request, "Serviço cadastrado com sucesso!")
        return redirect('dashboard:lista_servicos')

    return render(request, 'dashboard/service_form.html', {
        'form': form,
        'form_title': "Cadastrar Novo Serviço"
    })

# 📄 Listar serviços
@login_required
@user_passes_test(is_admin)
def lista_servicos(request):
    servicos = Service.objects.all().order_by('name')
    return render(request, 'dashboard/service_list.html', {'services': servicos})

# ✏️ Editar serviço
@login_required
@user_passes_test(is_admin)
def editar_servico(request, pk):
    servico = get_object_or_404(Service, id=pk)
    form = ServiceForm(request.POST or None, instance=servico)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Serviço atualizado com sucesso!")
        return redirect('dashboard:lista_servicos')

    return render(request, 'dashboard/service_form.html', {
        'form': form,
        'form_title': "Editar Serviço"
    })

# ❌ Excluir serviço
@login_required
@user_passes_test(is_admin)
def excluir_servico(request, pk):
    servico = get_object_or_404(Service, id=pk)

    if request.method == 'POST':
        servico.delete()
        messages.success(request, "Serviço excluído com sucesso!")
        return redirect('dashboard:lista_servicos')

    return render(request, 'dashboard/service_confirm_delete.html', {'servico': servico})
