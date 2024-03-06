"""
Дополнительная команда 'runapscheduler' для manage.py.
Созданные здесь задания можно также запустить из админки.
"""
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# for D9.5.1: send mail job
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


# задача по отправке писем на почту раз в 10 секунд.
def my_job():
    #  Your job processing logic here...
    send_mail(
        subject='[Django] Job mail',  # тема письма
        message='Hello from job!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=settings.RECIPIENT_LIST
    )


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            # CronTrigger то же, что и 'interval' в crutch-реализации
            trigger=CronTrigger(second="*/10"),  # срабатывает раз в 10 секунд
            id="my_job",  # уникальный id
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи,
            # которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
