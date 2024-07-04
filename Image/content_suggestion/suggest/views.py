
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import uploadimage, extractedtextserializer
from .models import Extractedtext
from .utils import Extract_keyword,Extract_text,match_keywords,extract_text_from_pdf
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class Imagekeywordview(APIView):
    def post(self,request,*args,**kwargs):
        serializer=uploadimage(data=request.data)

        if serializer.is_valid():
            image=serializer.validated_data.get('image',None)
            pdf=serializer.validated_data.get('pdf',None)


            if image:
                text=Extract_text(image)
            elif pdf:
                 # Save PDF to a temporary location
                pdf_path = default_storage.save(pdf.name, ContentFile(pdf.read()))
                pdf_full_path = os.path.join(default_storage.location, pdf_path)
                text = extract_text_from_pdf(pdf_full_path)
                # Clean up the saved file
                default_storage.delete(pdf_path)
            else:
                return Response ({"error": "No file provided"},status=status.HTTP_400_BAD_REQUEST)

            if text:
                keywords = Extract_keyword(text)

                extracted_text = Extractedtext.objects.create(
                    image=image, pdf=pdf ,text=text, keywords=keywords
                )
                matching_posts = []
                all_posts = Extractedtext.objects.exclude(id=extracted_text.id)
                for post in all_posts:
                    is_match, common_keywords = match_keywords(post.keywords, keywords)
                    if is_match:
                        matching_posts.append({
                            'id': post.id,
                            'image_url': post.image.url if post.image else None,
                            'pdf_url': post.pdf.url if post.pdf else None

                        })

                response_data = {
                    "extracted_text": extractedtextserializer(extracted_text).data,
                    "matching_posts": matching_posts
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No text found in the image."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request,*args , **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
# Create your views here.







