from .models import *
from django_grpc_framework.services import Service
from .serializers import *
class CommerceService(Service):
    """
    gRPC service that allows users to be retrieved or updated.
    """

    def GetList(self, request, context):
        """
        gRPC method to get user details.
        """
        # Extract the user ID from the request
        name= request.name
        id= request.id
        country = request.country
        commerce = None
        if(id):
            commerce = Commerce.objects.filter(id=id)
        elif(name):
            commerce = Commerce.objects.filter(name__contains = name,status=1)
        elif country:
            commerce = Commerce.objects.filter(country=country)
        
        res= []
        for i in commerce:
            body ={  }
            files = CommerceFiles.objects.filter(commerce= i.id,default = True)
            if(files.exists()):
                files= files[0]
                body["image"] = 'commerce/media/'+str(files.file)

            else:
                body["image"] = ''

            body["name"]= i.name
            res.append(body)
        final_res= {
            "commerce":res
        }
        return CommerceResponseProtoSerializer(final_res).message
    



                
        
