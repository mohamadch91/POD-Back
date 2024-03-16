#!/usr/bin/env python
import pika
import uuid
import json

class RpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq',credentials=pika.PlainCredentials(username='rabbitmq',password='rabbitmq')))

        self.channel = self.connection.channel(5)
        self.response = None
        self.corr_id = None
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
       

    def on_response(self, ch, method, props, body):


        if self.corr_id == props.correlation_id:
            self.response = body
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            
        # else:    
        #     ch.basic_ack(delivery_tag=0)

    def call(self, queue,data):
        self.response = None
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=data)
        while self.response is None:
            self.connection.process_data_events(time_limit=10)
        return self.response


def transfer(data,queue):
    
    rpc = RpcClient()
    response = rpc.call(queue=queue,data=data)
    rpc.connection.close()
    return(json.loads(response.decode('ascii')))