from .publish import get_commerce_list,get_service_list
# Create your views here.
from .permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SearchResponseSerializer
from .customResponse import CustomResponse,CustomMessage 

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        query = request.GET.get("query")
        if(query):
            commerces=get_commerce_list(query)
            print(commerces)
            services= get_service_list(query)
            final_response=[]
            if commerces.commerce and len(commerces.commerce)>0 :

                for i in commerces.commerce:
                    temp ={
                        "type" : "commerce",
                        "name": i.name,
                        "image": i.image,
                        "id": i.id
                    }
                    final_response.append(temp)
            if services.service and len(services.service)>0:
                for j in services.service:
                    temp ={
                        "type" : "service",
                        "name": i.name,
                        "image": i.image,
                        "id": i.id

                    }
                    final_response.append(temp)
            ser= SearchResponseSerializer(final_response,many=True)
            return CustomResponse(ser.data,status=status.HTTP_200_OK,message=CustomMessage(type=1))

        else:
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=""))
    

