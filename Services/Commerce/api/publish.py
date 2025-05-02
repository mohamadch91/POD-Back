#!/usr/bin/env python

import grpc 
from .rpc import base_info_pb2_grpc,base_info_pb2,user_pb2,user_pb2_grpc
import os
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
        response = stub.GetUser(request)
        return response

def get_info(data):
    with grpc.insecure_channel(BASE_INFO_ADDRESS) as channel:
        stub = base_info_pb2_grpc.BaseInfoControllerStub(channel)
        request =[]
        for i in data:
            request.append(base_info_pb2.BaseInfoRequest(name=i,id=data[i]))
        final_request = base_info_pb2.GetBaseInfoRequest(baseInfo=request)
        response = stub.GetInfo(final_request)
        return response