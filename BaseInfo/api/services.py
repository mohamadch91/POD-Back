from .models import *
from django_grpc_framework.services import Service
from .serializers import *
import grpc
from google.protobuf import empty_pb2
from django.shortcuts import get_object_or_404
import json
class BaseInfoService(Service):
    """
    gRPC service that allows users to be retrieved or updated.
    """

    def GetInfo(self, request, context):
        """
        gRPC method to get user details.
        """
        # Extract the user ID from the request
        base_info= request.baseInfo
        final_response =[]
        for i in base_info:
                if(i.name =="city"):
                        if(i.id):
                                city = get_object_or_404(City,id=i.id)
                                final_response.append({
                                        "key":"city",
                                        "value":city.value,
                                })
                              
                        else:
                                final_response.append({
                                        "key":"city",
                                        "value":None,
                                })
                if(i.name =="province"):
                        if(i.id):
                                province = get_object_or_404(Province,id=i.id)
                                
                                final_response.append({
                                        "key":"province",
                                        "value":province.value,
                                })
                        else:
                                final_response["province"] = None
                                final_response.append({
                                        "key":"province",
                                        "value":None,
                                })

                if(i.name =="commerceBrand"):
                        if(i.id):
                                brand = get_object_or_404(CommerceBrands,id=i.id)
                                final_response.append({
                                        "key":"brand",
                                        "value":brand.value,
                                })
                        else:
                                final_response.append({
                                        "key":"brand",
                                        "value":None,
                                })

                if(i.name =="commerceCategory"):
                        if(i.id):
                                cat = get_object_or_404(CommerceCategory,id=i.id)
                                final_response.append({
                                        "key":"category",
                                        "value":cat.value,
                                })
                        else:
                                final_response["category"] = None
                                final_response.append({
                                        "key":"category",
                                        "value":None,
                                })

                if(i.name =="serviceBrand"):
                        if(i.id):
                                brand = get_object_or_404(ServiceBrands,id=i.id)
                                final_response.append({
                                        "key":"brand",
                                        "value":brand.value,
                                })
                        else:

                                final_response.append({
                                        "key":"brand",
                                        "value":None,
                                })
                
                if(i.name =="serviceCategory"):
                        if(i.id):
                                cat = get_object_or_404(ServiceCategory,id=i.id)
                                final_response.append({
                                        "key":"category",
                                        "value":cat.value,
                                })
                        else:
                                final_response.append({
                                        "key":"category",
                                        "value":None,
                                })

                if(i.name =="sale"):
                        if(i.id):
                                sale = get_object_or_404(SaleMethod,id=i.id)
                                final_response.append({
                                        "key":"sale",
                                        "value":sale.value,
                                })
                        else:
                                final_response.append({
                                        "key":"sale",
                                        "value":None,
                                })

                if(i.name =="delivery"):
                        if(i.id):
                                sale = get_object_or_404(DeliveryMethod,id=i.id)
                                final_response.append({
                                        "key":"delivery",
                                        "value":sale.value,
                                })
                        else:
                                final_response.append({
                                        "key":"delivery",
                                        "value":None,
                                })
                if (i.name == "country"):
                        if(i.id):
                                country = get_object_or_404(Country,id=i.id)
                                final_response.append({
                                        "key":"country",
                                        "value":country.value,
                                })
                        else:
                                final_response.append({
                                        "key":"country",
                                        "value":None,
                                })
                                

        
        res ={
                "baseInfo":final_response
        }
        return BaseInfoRequestProtoSerializer(res).message
    



                
        
