from django.urls import path
from .views import AppointmentView, AppointmentCreatedView

urlpatterns = [
    path('', AppointmentView.as_view(), name='make_appointment'),
    path('created/', AppointmentCreatedView.as_view(), name='register'),
]
