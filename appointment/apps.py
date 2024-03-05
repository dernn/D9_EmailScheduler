from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment'

    # переопределим метод ready, чтобы вместе с приложением импортировать модуль 'signals'
    def ready(self):
        import appointment.signals

        # for D9.5: apscheduler
        from .tasks import send_mails
        from .scheduler import appointment_scheduler
        print('started')

        appointment_scheduler.add_job(
            id='mail send',
            func=send_mails,  # выполняемая функция
            trigger='interval',  # условие выполнения
            seconds=10,
        )
        appointment_scheduler.start()

