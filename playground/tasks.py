from time import sleep
from celery import shared_task

@shared_task
def notify_customers(message):
    print('sending 2388365 emails...')
    print(message)
    sleep(10)
    print('emails are sent')