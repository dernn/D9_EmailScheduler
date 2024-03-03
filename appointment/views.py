from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime

# импортируем функцию для массовой отправки писем уже менеджерам
from django.core.mail import mail_managers

from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # рассылка по группе MANAGERS
        mail_managers(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('appointments:register')


class AppointmentCreatedView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html', {})
