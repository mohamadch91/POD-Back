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
            service = Service.objects.filter(name__contains = name,status=1)
        elif country:
            service = Service.objects.filter(country=country)
        
        res= []
        for i in service:
            body ={  }
            files = ServiceFiles.objects.filter(service= i.id,default = True)
            if(files.exists()):
                files= files[0]
                body["image"] = 'service/media/'+str(files.file)

            else:
                body["image"] = ''
            body["name"]= i.name
            body['id'] = i.name
            res.append(body)
        final_res={
            "service": res
        }
        return ServiceResponseProtoSerializer(final_res).message
    



                
        

                
        
