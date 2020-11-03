from django.db import models
from django.contrib.auth.models import User

class Theme(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
