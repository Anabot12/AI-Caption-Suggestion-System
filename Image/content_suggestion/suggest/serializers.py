from rest_framework import serializers
from .models import Extractedtext

class extractedtextserializer(serializers.ModelSerializer):
    class Meta:
        model =Extractedtext
        fields=['id','image','pdf','text','keywords']

class uploadimage(serializers.Serializer):
    image = serializers.ImageField(required=False)
    pdf = serializers.FileField(required=False)

    class Meta:
        model=Extractedtext
        fields=['image','pdf']