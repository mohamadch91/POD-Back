from django.core.management.base import BaseCommand
import pika
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import *
from django.shortcuts import get_object_or_404
import json
def on_request(ch, method, props, body):
            final_response ={}

            ch.basic_publish(exchange='',
                            routing_key=props.reply_to,
                            properties=pika.BasicProperties(correlation_id = \
                                                                props.correlation_id),
                            body=str(final_response))
            ch.basic_ack(delivery_tag=method.delivery_tag)




class Command(BaseCommand):
    help = 'Description of my custom command'

    def handle(self, *args, **options):
        # Code for your custom command goes here
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq',credentials=pika.PlainCredentials(username='rabbitmq',password='rabbitmq')))

        channel = connection.channel(1)

        channel.queue_declare(queue='base_info')

    
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='base_info', on_message_callback=on_request)

        channel.start_consuming()