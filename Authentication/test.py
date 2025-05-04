
import json
import grpc 
import user_pb2,user_pb2_grpc
import os
import json
AUTH_ADDRESS = os.environ.get('AUTH_GRPC_ADDRESS', '[::]:50051')
BASE_INFO_ADDRESS = os.environ.get('BASE_INFO_GRPC_ADDRESS', '[::]:50052')

def get_user(id):
    with grpc.insecure_channel('localhost:50051') as channel:
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
            return user


        except Exception as e:
            print(f"Error: {e}")
            return None


print(get_user(2))