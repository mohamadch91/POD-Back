import grpc 
import user_pb2,user_pb2_grpc


with grpc.insecure_channel('localhost:8001') as channel:
    stub = user_pb2_grpc.UserControllerStub(channel)
    # get user by id
    response = stub.GetUser(user_pb2.GetUserRequest(id=1))
    print(response)
    # get by jwt 
    response = stub.Authentication(user_pb2.AuthenticationRequest(jwt=''))
    print(response)
    