from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime

# импортируем функцию для массовой отправки писем админам
from django.core.mail import mail_admins

from .models import Appointment

from EmailScheduler.settings import DEFAULT_FROM_EMAIL, RECIPIENT_LIST


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

        # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('appointments:register')


class AppointmentCreatedView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html', {})
