#!/usr/bin/env python

import grpc 
from .rpc import user_pb2,user_pb2_grpc
import os
import json
AUTH_ADDRESS = os.environ.get('AUTH_GRPC_ADDRESS', '[::]:50051')
BASE_INFO_ADDRESS = os.environ.get('BASE_INFO_GRPC_ADDRESS', '[::]:50052')

def authenticate(jwt):
    with grpc.insecure_channel(AUTH_ADDRESS) as channel:
        stub = user_pb2_grpc.UserControllerStub(channel)
        request = user_pb2.AuthenticationRequest(jwt=jwt)
        response = stub.Authentication(request)
        return response

    

def get_user(id):
    with grpc.insecure_channel(AUTH_ADDRESS) as channel:
        stub = user_pb2_grpc.UserControllerStub(channel)
        request = user_pb2.GetUserRequest(id=id)
        try:
            response = stub.GetUser(request)
            user= {}
            user['id'] = response.id
            user['phone'] = response.phone
            user['companyName'] = response.companyName
            user['first_name'] = response.first_name
            user['last_name'] = response.last_name


        except Exception as e:
            print(f"Error: {e}")
            return None

