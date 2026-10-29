from django.contrib import admin
from .models import Service, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'duration',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'name',
        'description',
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'service',
        'date',
        'time',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'date',
        'service',
    )

    search_fields = (
        'user__username',
        'service__name',
    )