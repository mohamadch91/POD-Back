from django.shortcuts import render

# Create your views here.


from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import IsAuthenticated,IsAdminUser
import copy

import json
from.customResponse import CustomResponse,CustomMessage
from.publish import get_user

class OrderViewAdmin(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        orders = Order.objects.all().order_by("-updated_at")
        total_count= len(orders)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            orders = orders[page*page_size:page_size*(page+1)]
        serializer = OrderSerializer(orders, many=True)
        res=[]
        for i in serializer.data:
            body={
                "id":i['id'],
                "user_id":get_user(i['user_id']),
                "order_type":i['order_type'],
                "amount":i['amount'],
                "status":i['status'],
                "created_at":i['created_at'],
                "updated_at":i['updated_at']
            }
            res.append(body)
        response = {
            "total_count": total_count,

            "orders": res
        }


        return CustomResponse(response,status=status.HTTP_200_OK,message=CustomMessage(type=1,data="سفارشات"))
    

    

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=1,data="سفارشات"))
    

class UserOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Order.objects.filter(user_id=request.user.id).order_by("-updated_at")
        serializer = OrderSerializer(queryset, many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=1,data="سفارشات"))


class AddOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = copy.deepcopy(request.data)
        user = request.user
        data['user_id'] = user.id
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="سفارشات"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data="سفارشات با خطا مواجه شد"))
    

class ChangeStatusView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        order_id = request.data.get('order_id')
        order_status = request.data.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = order_status
        order.save()
        return CustomResponse(OrderSerializer(order).data,status=status.HTTP_200_OK,message=CustomMessage(type=6,data="سفارشات"))
    

    