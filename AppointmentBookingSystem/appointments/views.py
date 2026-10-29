from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.db import IntegrityError, transaction

from .models import Service, Appointment
from .forms import BookingForm


def home_view(request):

    services = Service.objects.filter(
        is_active=True
    ).order_by('name')

    return render(request, 'appointments/home.html', {
        'services': services
    })

def service_list_view(request):

    services = Service.objects.filter(
        is_active=True
    ).order_by('name')

    return render(request, 'appointments/service_list.html', {
        'services': services
    })


@login_required
def book_appointment_view(request):

    initial = {}

    service_id = request.GET.get('service')

    if service_id:
        try:
            service = Service.objects.get(
                id=service_id,
                is_active=True
            )
            initial['service'] = service
        except Service.DoesNotExist:
            pass

    if request.method == 'POST':

        form = BookingForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)
            appointment.user = request.user

            existing_appointment = Appointment.objects.filter(
                date=appointment.date,
                time=appointment.time
            ).exclude(
                status='Cancelled'
            ).exists()

            if existing_appointment:

                form.add_error(
                    None,
                    'This time slot is already booked.'
                )

            else:

                appointment.save()

                return redirect('my_appointments')

    else:

        form = BookingForm(initial=initial)

    return render(request, 'appointments/book.html', {
        'form': form
    })

@login_required
def my_appointments_view(request):

    today = timezone.localdate()

    upcoming = Appointment.objects.filter(
        user=request.user,
        date__gte=today,
        status__in=['Pending', 'Confirmed']
    ).select_related(
        'service'
    ).order_by(
        'date',
        'time'
    )

    past = Appointment.objects.filter(
        user=request.user
    ).filter(
        Q(date__lt=today) |
        Q(status='Completed') |
        Q(status='Cancelled')
    ).select_related(
        'service'
    ).order_by(
        '-date',
        '-time'
    )

    return render(request, 'appointments/my_appointments.html', {
        'upcoming': upcoming,
        'past': past,
    })
@login_required
def cancel_appointment_view(request, id):

    appointment = get_object_or_404(
        Appointment,
        id=id,
        user=request.user
    )

    today = timezone.localdate()

    if request.method == 'POST':

        if (
            appointment.status not in ['Pending', 'Confirmed']
            or appointment.date < today
        ):
            return redirect('my_appointments')

        appointment.status = 'Cancelled'
        appointment.save()

        return redirect('my_appointments')

    return render(request, 'appointments/cancel.html', {
        'appointment': appointment
    })

@login_required
def dashboard_view(request):

    upcoming_count = Appointment.objects.filter(
        user=request.user,
        date__gte=timezone.localdate()
    ).exclude(
        status='Cancelled'
    ).count()

    completed_count = Appointment.objects.filter(
        user=request.user,
        status='Completed'
    ).count()

    cancelled_count = Appointment.objects.filter(
        user=request.user,
        status='Cancelled'
    ).count()

    pending_count = Appointment.objects.filter(
        user=request.user,
        status='Pending'
    ).count()

    next_appointment = Appointment.objects.filter(
        user=request.user,
        date__gte=timezone.localdate()
    ).exclude(
        status='Cancelled'
    ).order_by(
        'date',
        'time'
    ).first()

    return render(request, 'appointments/dashboard.html', {
        'upcoming_count': upcoming_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'pending_count': pending_count,
        'next_appointment': next_appointment,
    })