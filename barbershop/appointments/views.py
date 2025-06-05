from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from datetime import datetime, date, time, timedelta
from django.http import JsonResponse
from barbershop.users.models import User
from django.utils.timezone import now
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError
from datetime import datetime, date, time, timedelta
import logging
logger = logging.getLogger(__name__)

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
            appointment.status = 'pendente'

            # 🔍 Verifica se já existe um agendamento no mesmo horário para o mesmo barbeiro (exceto cancelados)
            conflito = Appointment.objects.filter(
                barber=appointment.barber,
                date=appointment.date,
                time=appointment.time
            ).exclude(status='cancelado').exists()

            if conflito:
                messages.error(request, "Já existe um agendamento nesse horário.")
                return redirect('appointments:schedule')

            try:
                appointment.save()
                messages.success(request, "Agendamento realizado com sucesso.")
                return redirect('appointments:list')
            except IntegrityError:
                messages.error(request, "Erro ao salvar o agendamento. Verifique os dados e tente novamente.")
                return redirect('appointments:schedule')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/schedule.html', {'form': form})
@login_required
def list_all(request):
    agendamentos = Appointment.objects.all().order_by('-date', '-time')
    return render(request, 'appointments/list_all.html', {'appointments': agendamentos})

@login_required
def editar_agendamento(request, pk):
    if request.user.is_staff or request.user.is_barber:
        agendamento = get_object_or_404(Appointment, pk=pk)
    else:
        agendamento = get_object_or_404(Appointment, pk=pk, client=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('appointments:list')
    else:
        form = AppointmentForm(instance=agendamento)

    return render(request, 'appointments/editar_agendamento.html', {'form': form})


@login_required
def concluido(request, pk):
    agendamento = get_object_or_404(Appointment, pk=pk)

    logger.info(f"Agendamento concluido: {agendamento}")  # Vai para o log do servidor
    agendamento.status = 'concluido'
    agendamento.save()
    messages.success(request, "Agendamento concluido.")
    return redirect('appointments:list')


@login_required
def confirmar_agendamento(request, pk):
    agendamento = get_object_or_404(Appointment, pk=pk)

    if agendamento.barber != request.user:
        messages.error(request, "Você não tem permissão para confirmar este agendamento.")
        return redirect('appointments:list_all')

    logger.info(f"Agendamento confirmado: {agendamento}")  # Vai para o log do servidor
    agendamento.status = 'confirmado'
    agendamento.save()
    messages.success(request, "Agendamento confirmado com sucesso.")
    return redirect('appointments:list_all')


# Gera horários disponíveis com intervalo de 45 minutos

def available_times(barber, date_selected):
    start_time = time(9, 0)
    end_time = time(18, 0)
    interval = timedelta(minutes=45)

    now = datetime.now()

    current_time = datetime.combine(date_selected, start_time)
    end_datetime = datetime.combine(date_selected, end_time)

    # busca agendamentos válidos (não cancelados)
    appointments = Appointment.objects.filter(barber=barber, date=date_selected).exclude(status='cancelado')
    booked_times = set(a.time for a in appointments)

    available = []
    while current_time <= end_datetime:
        t = current_time.time()

        # 💡 Filtra horários passados se for o dia de hoje
        if date_selected == date.today() and current_time < now:
            current_time += interval
            continue

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
    if request.user.is_staff or request.user.is_barber:
        agendamento = get_object_or_404(Appointment, pk=pk)
    else:
        agendamento = get_object_or_404(Appointment, pk=pk, client=request.user)
        
    if request.method == 'POST':
        agendamento.status = 'cancelado'
        agendamento.save()
        return redirect('appointments:list')

    return render(request, 'appointments/cancelar_confirmacao.html', {'agendamento': agendamento})
