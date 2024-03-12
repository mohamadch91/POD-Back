from django.core.management.base import BaseCommand
import pika
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import *
from django.shortcuts import get_object_or_404
import json
def on_verify_request(ch, method, props, body):
            # n = int(body)

            JWT_authenticator = JWTAuthentication()
            # authenitcate() verifies and decode the token
            # if token is invalid, it raises an exception and returns 401
            final_response ={}

            try:
                v_token = JWT_authenticator.get_validated_token(body)
                response = JWT_authenticator.get_user(v_token)
                if response is not None:
                    # unpacking
                    final_response['user'] = json.dumps({
                         "id": response.id,
                         "phone": response.phone
                    })
                    final_response['token'] = v_token['token_type']
            except:
                 print('invalid')
            
            ch.basic_publish(exchange='',
                            routing_key=props.reply_to,
                            properties=pika.BasicProperties(correlation_id = \
                                                                props.correlation_id),
                            body=json.dumps(final_response))
            ch.basic_ack(delivery_tag=method.delivery_tag)
def on_user_detail_request(ch, method, props, body):
            user_id = int(body)
            final_response ={}
            try:
                user= get_object_or_404(User,pk =user_id)
                if(isinstance(user, LegalUser)):
                    serializer = LegalUserSerializer(user)
                else:
                        serializer =RealUserSerializer(user)
                
                final_response = json.dumps(serializer.data)
            except Exception as e:
               print(e)
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

        channel = connection.channel()

        channel.queue_declare(queue='user_data')
        channel.queue_declare(queue='verify')

    
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='user_data', on_message_callback=on_user_detail_request,auto_ack=False)
        channel.basic_consume(queue='verify', on_message_callback=on_verify_request,auto_ack=False)

        print("started")
        channel.start_consuming()