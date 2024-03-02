from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
# импортируем класс для создания объекта письма с html
from django.core.mail import EmailMultiAlternatives
# импортируем функцию, которая срендерит наш html в текст
from django.template.loader import render_to_string
from .models import Appointment

# settings можно импортировать из django.conf
# from django.conf import settings
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

        # получаем наш html в виде строки
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,  # appointment передаем в контекст
            }
        )

        # инстанс EmailMultiAlternatives похож на метод send_mail()
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%m-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email=DEFAULT_FROM_EMAIL,
            to=RECIPIENT_LIST,  # это то же, что и recipients_list
        )
        # метод, что передает строку-html в объявленный инстанс
        msg.attach_alternative(html_content, "text/html")
        msg.send()  # отсылаем

        return redirect('appointments:register')


class AppointmentCreatedView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html', {})
