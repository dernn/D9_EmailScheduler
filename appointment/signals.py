from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.core.mail import mail_managers
from appointment.models import Appointment


# создаём функцию-обработчик с параметрами под регистрацию сигнала
def notify_managers_appointment(sender, instance, created, **kwargs):
    subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )


# аналог декоратора @receiver
# конектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
post_save.connect(notify_managers_appointment, sender=Appointment)