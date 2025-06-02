from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from datetime import datetime, date, time, timedelta
from django.http import JsonResponse
from barbershop.users.models import User
from django.utils.timezone import now
from django.db.models import Q


@login_required
def list_appointments(request):
    # Exibe apenas agendamentos pendentes e futuros
    appointments = Appointment.objects.filter(
        Q(status='pendente') | Q(status='confirmado'),
        client=request.user,
        date__gte=date.today()
    ).order_by('date', 'time')

    return render(request, 'appointments/list.html', {'appointments': appointments})


@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.status = 'pendente'  # define status padrão
            appointment.save()
            return redirect('appointments:list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/schedule.html', {'form': form})


@login_required
def editar_agendamento(request, pk):
    agendamento = get_object_or_404(Appointment, pk=pk, client=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('appointments:list')
    else:
        form = AppointmentForm(instance=agendamento)

    return render(request, 'appointments/editar_agendamento.html', {'form': form})


# Gera horários disponíveis com intervalo de 45 minutos
def available_times(barber, date):
    start_time = time(9, 0)
    end_time = time(18, 0)
    interval = timedelta(minutes=45)

    current_time = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)

    appointments = Appointment.objects.filter(barber=barber, date=date)
    booked_times = set(a.time for a in appointments)

    available = []
    while current_time <= end_datetime:
        t = current_time.time()
        if t not in booked_times:
            available.append(t)
        current_time += interval

    return available


@login_required
def horarios_disponiveis(request):
    date_str = request.GET.get('date')
    barber_id = request.GET.get('barber_id')

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        if date_obj < date.today():
            return JsonResponse({'times': []})  # impede datas passadas
        barber = User.objects.get(id=barber_id, is_barber=True)
    except (ValueError, User.DoesNotExist):
        return JsonResponse({'times': []})

    times = available_times(barber, date_obj)
    formatted_times = [t.strftime('%H:%M') for t in times]

    return JsonResponse({'times': formatted_times})

@login_required
def historico_agendamentos(request):
    historico = Appointment.objects.filter(
        client=request.user
    ).exclude(status='pendente').order_by('-date', '-time')

    return render(request, 'appointments/historico.html', {'appointments': historico})


@login_required
def cancelar_agendamento(request, pk):
    agendamento = get_object_or_404(Appointment, pk=pk, client=request.user)

    if request.method == 'POST':
        agendamento.status = 'cancelado'
        agendamento.save()
        return redirect('appointments:list')

    return render(request, 'appointments/cancelar_confirmacao.html', {'agendamento': agendamento})
