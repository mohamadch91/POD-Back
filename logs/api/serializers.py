from rest_framework import serializers
from .models import *

class ConsultationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationRequest
        fields = '__all__'

class PermiumRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermiumRequest
        fields = '__all__'


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

