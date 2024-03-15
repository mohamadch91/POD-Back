from django.core.management.base import BaseCommand
import pika
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import *
from django.shortcuts import get_object_or_404
import json
def on_request(ch, method, props, body):
            data = json.loads(body)
            final_response ={}
            for i in data:
                if(i =="city"):
                        if(data[i]):
                                city = get_object_or_404(City,id=data[i])
                                final_response["city"] = city.value
                        else:
                                final_response["city"] = None
                if(i =="province"):
                        if(data[i]):
                                province = get_object_or_404(Province,id=data[i])
                                final_response["province"] = province.value
                        else:
                                final_response["province"] = None

                if(i =="commerceBrand"):
                        if(data[i]):
                                brand = get_object_or_404(CommerceBrands,id=data[i])
                                final_response["brand"] = brand.value
                        else:
                                final_response["brand"] = None

                if(i =="commerceCategory"):
                        if(data[i]):
                                cat = get_object_or_404(CommerceCategory,id=data[i])
                                final_response["category"] = cat.value
                        else:
                                final_response["category"] = None

                if(i =="serviceBrand"):
                        if(data[i]):
                                brand = get_object_or_404(ServiceBrands,id=data[i])
                                final_response["brand"] = brand.value
                        else:

                                final_response["brand"] = None
                
                if(i =="serviceCategory"):
                        if(data[i]):
                                cat = get_object_or_404(ServiceCategory,id=data[i])
                                final_response["category"] = cat.value
                        else:
                                final_response["category"] = None

                    
            ch.basic_publish(exchange='',
                            routing_key=props.reply_to,
                            properties=pika.BasicProperties(correlation_id = \
                                                                props.correlation_id),
                            body=json.dumps(final_response))
            ch.basic_ack(delivery_tag=method.delivery_tag)


class Command(BaseCommand):
    help = 'Description of my custom command'

    def handle(self, *args, **options):
        # Code for your custom command goes here
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq',credentials=pika.PlainCredentials(username='rabbitmq',password='rabbitmq')))

        channel = connection.channel()

        channel.queue_declare(queue='base_info')

    
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='base_info', on_message_callback=on_request,auto_ack=False)

        channel.start_consuming()