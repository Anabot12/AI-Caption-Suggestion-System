from django.db import models

class Extractedtext(models.Model):
    image=models.ImageField(upload_to='images/')
    text=models.TextField()
    keywords=models.JSONField()




    def __str__(self):
        return self.text[:50]
# Create your models here.
