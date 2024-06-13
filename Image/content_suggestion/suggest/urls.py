from django.urls import path
from .views import Imagekeywordview

urlpatterns = [
    path('keywords/', Imagekeywordview.as_view(), name='keywords'),
    
]
