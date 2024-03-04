from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment'

    # переопределим метод ready, чтобы вместе с приложением импортировать модуль 'signals'
    def ready(self):
        import appointment.signals
