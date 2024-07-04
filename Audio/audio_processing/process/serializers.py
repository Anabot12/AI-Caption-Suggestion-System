from rest_framework import serializers
from .models import Audio

class Audioserializer(serializers.ModelSerializer):
    class Meta:
        model=Audio
        fields=['id','audio','text','keywords']

class Audioupload(serializers.Serializer):
    audio=serializers.FileField()