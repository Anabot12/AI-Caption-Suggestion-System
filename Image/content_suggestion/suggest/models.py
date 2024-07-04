from django.db import models

class Extractedtext(models.Model):
    image=models.ImageField(upload_to='images/',blank=True,null=True)
    pdf= models.FileField(upload_to='pdf/',blank=True,null=True)
    text=models.TextField()
    keywords=models.JSONField()

    def __str__(self):
        return f"Image ID: {self.id}, Keywords: {self.keywords}"
# Create your models here.
