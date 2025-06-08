from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm  # Adicione esta importação
from barbershop.users.models import User
from .models import CarouselImage


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



def home(request):
    carousel_images = CarouselImage.objects.all()
    return render(request, 'landing.html', {'carousel_images': carousel_images})

