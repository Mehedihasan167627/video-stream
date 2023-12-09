from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self) -> str:
        return self.title 