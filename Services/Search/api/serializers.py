from rest_framework import serializers



  

class SearchResponseSerializer(serializers.ModelSerializer):
    name= serializers.CharField()
    image = serializers.CharField()
    type = serializers.CharField()
