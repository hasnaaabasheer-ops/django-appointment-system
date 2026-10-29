from datetime import time as dt_time
from django import forms
from django.utils import timezone
from .models import Appointment, Service


class BookingForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            'service',
            'date',
            'time',
            'note',
        ]

        widgets = {
            'service': forms.Select(attrs={
                'class': 'form-select',
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),

            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add a short note (optional)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['service'].queryset = Service.objects.filter(
            is_active=True
        )

    def clean_date(self):
        date = self.cleaned_data.get('date')
        today = timezone.localdate()

        if date and date < today:
            raise forms.ValidationError(
                'You cannot book an appointment for a past date.'
            )

        return date

    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')

        if selected_time:
            if not dt_time(9, 0) <= selected_time <= dt_time(18, 0):
                raise forms.ValidationError(
                    'Appointments are available only between 9:00 AM and 6:00 PM.'
                )

        if date and selected_time:

            existing = Appointment.objects.filter(
                date=date,
                time=selected_time
            ).exclude(
                status='Cancelled'
            ).exists()

            if existing:
                raise forms.ValidationError(
                    'This time slot is already booked.'
                )

        return cleaned_data