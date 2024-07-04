from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Audioserializer, Audioupload
from .models import Audio
from .utils import audio_process, extract_keywords_from_text,matching_keywords

class AudioTranscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Audioupload(data=request.data)
        if serializer.is_valid():
            audio = serializer.validated_data['audio']

            # Transcribe audio to text
        try:
            text = audio_process(audio)

            # Extract keywords from the transcribed text
            keywords = extract_keywords_from_text(text)

            # Save the transcribed text and keywords to the database
            transcribed_audio_instance = Audio.objects.create(audio=audio,
                                                              text=text,
                                                              keywords=keywords)

            similar_posts = matching_keywords(keywords)

            # Serialize response data
            response_serializer = Audioserializer(transcribed_audio_instance)
            response_data = response_serializer.data
            response_data['similar_posts'] = similar_posts

            return Response(response_data, status=status.HTTP_200_OK)
        
        except RuntimeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
