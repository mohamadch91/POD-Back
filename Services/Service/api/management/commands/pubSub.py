from django.core.management.base import BaseCommand
import pika
import os


class Command(BaseCommand):
    help = 'Description of my custom command'

    def handle(self, *args, **options):
        # Code for your custom command goes here
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='0.0.0.0',credentials=pika.PlainCredentials(username='rabbitmq',password='rabbitmq')))
        channel = connection.channel(1)
        channel.queue_declare(queue='service')


    
    