from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings


@shared_task
def new_order(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order № {}'.format(order_id)
    message = 'Dear {},\n\nYou have successfully make an order.\
                    Your order id is {}.'.format(order.user_name,
                                                 order.id)
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          ['ksyutsutsalevich@mail.ru',])
    return mail_sent
