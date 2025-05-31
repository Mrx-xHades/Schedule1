from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from datetime import datetime, time, timedelta
from django.http import JsonResponse
from barbershop.users.models import User


@login_required
def list_appointments(request):
    appointments = Appointment.objects.filter(client=request.user)
    return render(request, 'appointments/list.html', {'appointments': appointments})


@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()
            return redirect('appointments:list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/schedule.html', {'form': form})


# ✅ View de edição integrada
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


# Função para gerar horários disponíveis
def available_times(barber, date):
    # Horário de trabalho: 09:00 às 18:00
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


# Endpoint AJAX que retorna os horários livres
@login_required
def horarios_disponiveis(request):
    date_str = request.GET.get('date')
    barber_id = request.GET.get('barber_id')

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        barber = User.objects.get(id=barber_id, is_barber=True)
    except (ValueError, User.DoesNotExist):
        return JsonResponse({'times': []})

    times = available_times(barber, date)
    formatted_times = [t.strftime('%H:%M') for t in times]

    return JsonResponse({'times': formatted_times})


# ✅ View para cancelar agendamento
@login_required
def cancelar_agendamento(request, pk):
    agendamento = get_object_or_404(Appointment, pk=pk, client=request.user)
    
    if request.method == 'POST':
        agendamento.delete()
        return redirect('appointments:list')
    
    return render(request, 'appointments/cancelar_confirmacao.html', {'agendamento': agendamento})
