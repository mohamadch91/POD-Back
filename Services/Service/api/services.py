from django_grpc_framework.services import Service as service
from .models import *
from .serializers import *
class CustomService(service):
    """
    gRPC service that allows users to be retrieved or updated.
    """

    def GetList(self, request, context):
        """
        gRPC method to get user details.
        """
        # Extract the user ID from the request
        """
        gRPC method to get user details.
        """
        # Extract the user ID from the request
        name= request.name
        id= request.id
        country = request.country
        service = None
        if(id):
            service = Service.objects.filter(id=id)
        elif(name):
            service = Service.objects.filter(name__contains = name)
        elif country:
            service = Service.objects.filter(country=country)
        
        res= []
        for i in service:
            body ={  }
            files = ServiceFiles.objects.filter(service= i.id,default = True)
            files= files[0]
            body["image"] = 'service/media/'+str(files.file)
            body["name"]= i.name
            res.append(body)
        return ServiceResponseProtoSerializer(res).message
    



                
        

                
        
