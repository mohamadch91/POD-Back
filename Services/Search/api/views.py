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
            services= get_service_list(query)
            final_response=[]
            for i in commerces:
                i["type"] = "commerce"
                final_response.append(i)
            for j in services:
                j["type"] = "service"
                final_response.append(j)
            ser= SearchResponseSerializer(final_response)
            return CustomResponse(ser.data,status=status.HTTP_200_OK,message=CustomMessage(type=1))

        else:
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2))
    