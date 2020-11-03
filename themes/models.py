from django.db import models

class Theme(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
