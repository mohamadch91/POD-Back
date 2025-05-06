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

class OrderViewAdmin(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=1,data="سفارشات"))
    

    

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
        queryset = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(queryset, many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=1,data="سفارشات"))


class AddOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = copy.deepcopy(request.data)
        print(request.user)
        user,token = request.user
        user= json.loads(user)
        data['user_id'] = user['id']
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="سفارشات"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data="سفارشات با خطا مواجه شد"))
    

class ChangeStatusView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        order_id = request.data.get('order_id')
        status = request.data.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = status
        order.save()
        return CustomResponse(OrderSerializer(order).data,status=status.HTTP_200_OK,message=CustomMessage(type=6,data="سفارشات"))
    

    