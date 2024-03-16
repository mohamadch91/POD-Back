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
        # self.corr_id = None
        self.corr_id = str(uuid.uuid4())

        self.name= queue_name
        self .channel.basic_qos(prefetch_count=0)
        self.channel.basic_consume(
            queue=self.name,
            on_message_callback=self.on_response,
            auto_ack=False)
       

    def on_response(self, ch, method, props, body):
        print(body,"body")
        print( props.correlation_id,"props corr")
        print( self.corr_id,"self corr")

        if self.corr_id == props.correlation_id:
            self.response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        else:    
            ch.basic_ack(delivery_tag=0)

    def call(self, queue,data):
        self.response = None
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            properties=pika.BasicProperties(
                reply_to=self.name,
                correlation_id=self.corr_id,
            ),
            body=data)
        while self.response is None:
            print(self.response,"response")
            self.connection.process_data_events(time_limit=None)
        return self.response


def transfer(data,queue,source):
    
    rpc = RpcClient(queue_name=source)
    response = rpc.call(queue=queue,data=data)
    print("closed")
    rpc.connection.close()
    return(json.loads(response.decode('ascii')))