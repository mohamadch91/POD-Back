from rest_framework import serializers



class SearchResponseSerializer(serializers.Serializer):
    name= serializers.CharField()
    image = serializers.CharField()
    type = serializers.CharField()
    id= serializers.IntegerField()
