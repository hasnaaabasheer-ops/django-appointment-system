from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    duration = models.PositiveIntegerField(
        default=30
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    date = models.DateField()

    time = models.TimeField()

    note = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    
    def __str__(self):
        return f'{self.user.username} - {self.service.name} - {self.date} {self.time}'