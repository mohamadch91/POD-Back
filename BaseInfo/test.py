import grpc 
import base_info_pb2_grpc,base_info_pb2


with grpc.insecure_channel('localhost:50052') as channel:
    stub = base_info_pb2_grpc.BaseInfoControllerStub(channel)
    # get user by id
    request = {
        "baseInfo" :[
            {
                "name":"city",
                "id":1
            },
            {
                "name":"province",
                "id":1
            },
            {
                "name":"commerceBrand",
                "id":1
            },
            {
                "name":"commerceCategory",
                "id":1
            },
            {
                "name":"serviceBrand",
                "id":1
            },
            {
                "name":"serviceCategory",
                "id":1
            },
           
        ]
    }
    request = base_info_pb2.BaseInfoRequest(name="city",id=1)
    

    response = stub.GetInfo(base_info_pb2.GetBaseInfoRequest(baseInfo=[request]))
    print(response.baseInfo)
  

    