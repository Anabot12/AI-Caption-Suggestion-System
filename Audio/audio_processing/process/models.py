from django.db import models



class Audio(models.Model):
    audio=models.FileField(upload_to='audio/')
    text= models.TextField()
    keywords=models.JSONField()

# Create your models here.
