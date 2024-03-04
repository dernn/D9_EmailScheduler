from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from appointment.models import Appointment


# первым аргументом передается сигнал, а вторым модель
@receiver(post_save, sender=Appointment)
# создаём функцию-обработчик с параметрами под регистрацию сигнала
def notify_managers_appointment(sender, instance, created, **kwargs):
    # в зависимости от того, есть ли такой объект уже в базе данных или нет, тема письма будет разная
    if created:  # если создаётся
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:  # если редактируется
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )

# с помощью сигнала request_finished можно построить систему, которая будет отслеживать и записывать в базу данных,
# все действия пользователей на вашем сайте.
