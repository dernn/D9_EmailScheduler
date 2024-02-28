from django.shortcuts import render, redirect, reverse
from django.views import View
from datetime import datetime
# отправление электронных писем
from django.core.mail import send_mail
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

        # отправка письма
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%m-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email=DEFAULT_FROM_EMAIL,  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=RECIPIENT_LIST  # здесь list получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('appointments:register')


class AppointmentCreatedView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html', {})
