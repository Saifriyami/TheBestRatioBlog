from django.db import models

class UploadedFile(models.Model):
    title = models.CharField(max_length=255, unique=True)
    path = models.CharField(max_length=1024, unique=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
