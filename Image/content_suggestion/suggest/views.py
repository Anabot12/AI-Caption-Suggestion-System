
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import uploadimage, extractedtextserializer
from .models import Extractedtext
from .utils import Extract_keyword,Extract_text


class Imagekeywordview(APIView):
    def post(self,request,*args,**kwargs):
        serializer=uploadimage(data=request.data)
        if serializer.is_valid():
            image=serializer.validated_data['image']
            text=Extract_text(image)
            keywords=Extract_keyword(text)

            extract_text_1=Extractedtext.objects.create(image=image, text=text,keywords=keywords)

            response_serializer=extractedtextserializer(extract_text_1)
            return Response(response_serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)


    def get(self,request,*args , **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
# Create your views here.







