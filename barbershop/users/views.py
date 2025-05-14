from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm  # Adicione esta importação
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    print("Tentando renderizar users/register.html")
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')