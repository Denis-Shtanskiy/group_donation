from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_payment_successfully_created_email_task(request):
    send_mail(
        'Информация о платеже',
        f'Ваш платеж, на сумму {request.data.get("amount")} успешно создан!',
        None,
        [request.user.email],
        fail_silently=True
    )


@shared_task
def send_collection_successfully_created_email_task(request):
    send_mail(
        'Информация о сборе',
        f'Ваш сбор {request.data.get("name")}, '
        f'на сумму {request.data.get("planned_amount")} успешно создан',
        None,
        recipient_list=[request.author.email],
        fail_silently=True,
    )
