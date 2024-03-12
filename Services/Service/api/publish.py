#!/usr/bin/env python
import pika
import uuid
import json

class RpcClient(object):

    def __init__(self,queue_name):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq',credentials=pika.PlainCredentials(username='rabbitmq',password='rabbitmq')))

        self.channel = self.connection.channel()
        self.response = None
        self.corr_id = None
        self.name= queue_name

        self.channel.basic_consume(
            queue=self.name,
            on_message_callback=self.on_response,
            auto_ack=False)
       

    def on_response(self, ch, method, props, body):

        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, queue,data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        print(self.corr_id)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            properties=pika.BasicProperties(
                reply_to=self.name,
                correlation_id=self.corr_id,
            ),
            body=data)
        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return self.response


def auth(data,queue,source):
    rpc = RpcClient(queue_name=source)
    response = rpc.call(queue=queue,data=data)
    rpc.connection.close()

    return(json.loads(response.decode('ascii')))