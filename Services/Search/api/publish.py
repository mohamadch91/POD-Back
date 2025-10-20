#!/usr/bin/env python

import grpc 
from .rpc import user_pb2,user_pb2_grpc,commerce_pb2,commerce_pb2_grpc,service_pb2,service_pb2_grpc
import os
import json
AUTH_ADDRESS = os.environ.get('AUTH_GRPC_ADDRESS', '[::]:50051')
BASE_INFO_ADDRESS = os.environ.get('BASE_INFO_GRPC_ADDRESS', '[::]:50052')
COMMERCE_ADRESS= os.environ.get("COMMERCE_GRPC_ADDRESS","[::]:50053")
SERVICE_ADRESS= os.environ.get("SERVICE_GRPC_ADDRESS","[::]:50054")


def authenticate(jwt):
    with grpc.insecure_channel(AUTH_ADDRESS) as channel:
        stub = user_pb2_grpc.UserControllerStub(channel)
        request = user_pb2.AuthenticationRequest(jwt=jwt)
        try:
            response = stub.Authentication(request)
            return response
        except Exception as e:
            print(f"Error: {e}")
            return None

    


def get_commerce_list(query):
    print(COMMERCE_ADRESS)
    with grpc.insecure_channel(COMMERCE_ADRESS) as channel:
        stub = commerce_pb2_grpc.CommerceControllerStub(channel)
        
        request = commerce_pb2.GetCommerceRequest(name =query,id=None,country=None)
        try:
            response = stub.GetList(request)
            return response
        except Exception as e:
            print(f"Error: {e}")
            return None
        
def get_service_list(query):
    with grpc.insecure_channel(SERVICE_ADRESS) as channel:
        stub = service_pb2_grpc.ServiceControllerStub(channel)
        request = service_pb2.GetServiceRequest(name =query,id=None,country=None)

        
        try:
            response = stub.GetList(request)
            return response
        except Exception as e:
            print(f"Error: {e}")
            return None
        

        
