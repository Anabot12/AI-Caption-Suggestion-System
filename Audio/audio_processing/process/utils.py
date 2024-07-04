import spacy
import speech_recognition as sr
from pydub import AudioSegment
import os
from .models import Audio

nlp=spacy.load("en_core_web_sm")

def audio_process(audio_file):

    recognizer = sr.Recognizer()
    audio_format = audio_file.name.split('.')[-1].lower()
    audio_path = audio_file.temporary_file_path() if hasattr(audio_file, 'temporary_file_path') else None

    # Convert audio to WAV if it's not already in a supported format
    if audio_format not in ['wav', 'aiff', 'flac']:
        audio = AudioSegment.from_file(audio_file, format=audio_format)
        audio_path = audio_file.name.split('.')[0] + '.wav'
        audio.export(audio_path, format='wav')

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = ""
        except sr.RequestError as e:
            raise RuntimeError(f"Could not request results from Google Speech Recognition service; {e}")

    # Clean up the temporary file if it was created
    if audio_format not in ['wav', 'aiff', 'flac']:
        os.remove(audio_path)

    return text

def extract_keywords_from_text(text):
    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks if len(chunk.text) > 1]
    return keywords

def matching_keywords(new_keywords):
    all_posts = Audio.objects.all()
    matching_posts = []
    for post in all_posts:
        existing_keywords = post.keywords
        match_count = sum(1 for keyword in new_keywords if keyword in existing_keywords)
        if match_count >= len(new_keywords) * 0.5:
            matching_posts.append(post.id)

    return matching_posts


