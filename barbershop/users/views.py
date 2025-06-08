from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from barbershop.users.models import User
from .models import CarouselImage
from .forms import CarouselImageForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test


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
    carousel_images = CarouselImage.objects.all().order_by('-created_at')[:10]
    return render(request, 'landing.html', {'carousel_images': carousel_images})


def is_barber(user):
    return user.is_authenticated and (user.is_barber or user.is_staff)


@login_required
@user_passes_test(is_barber)
def carousel_list(request):
    images = CarouselImage.objects.all().order_by('-created_at')
    return render(request, 'carousel/list.html', {'images': images})

@login_required
@user_passes_test(is_barber)
def carousel_add(request):
    if request.method == 'POST':
        form = CarouselImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('carousel_list')
    else:
        form = CarouselImageForm()
    return render(request, 'carousel/form.html', {'form': form})

@login_required
@user_passes_test(is_barber)
def carousel_edit(request, pk):
    image = get_object_or_404(CarouselImage, pk=pk)
    if request.method == 'POST':
        form = CarouselImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('carousel_list')
    else:
        form = CarouselImageForm(instance=image)
    return render(request, 'carousel/form.html', {'form': form})

@login_required
@user_passes_test(is_barber)
def carousel_delete(request, pk):
    image = get_object_or_404(CarouselImage, pk=pk)
    image.delete()
    return redirect('carousel_list')

