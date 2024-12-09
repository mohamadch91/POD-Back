from django.shortcuts import render

# Create your views here.


from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import IsAuthenticatedM
import copy


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedM]

    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user.id)
        return queryset
    

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticatedM]
    def get(self, request):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    

class UserOrderView(APIView):
    permission_classes = [IsAuthenticatedM]
    def get(self, request):
        queryset = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class AddOrderView(APIView):
    permission_classes = [IsAuthenticatedM]
    def post(self, request):
        data = copy.deepcopy(request.data)
        data['user_id'] = request.user.id
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangeStatusView(APIView):
    permission_classes = [IsAuthenticatedM]
    def post(self, request):
        order_id = request.data.get('order_id')
        status = request.data.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = status
        order.save()
        return Response(OrderSerializer(order).data)
    

    