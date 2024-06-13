from rest_framework import serializers
from .models import Extractedtext

class extractedtextserializer(serializers.ModelSerializer):
    class Meta:
        model =Extractedtext
        fields=['id','image','text','keywords']

class uploadimage(serializers.Serializer):
    image=serializers.ImageField()