from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home_view,
        name='home'
    ),

    path(
        'services/',
        views.service_list_view,
        name='service_list'
    ),

    path(
        'book/',
        views.book_appointment_view,
        name='book'
    ),

    path(
        'my-appointments/',
        views.my_appointments_view,
        name='my_appointments'
    ),

    path(
        'appointment/<int:id>/cancel/',
        views.cancel_appointment_view,
        name='cancel_appointment'
    ),

    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),

]