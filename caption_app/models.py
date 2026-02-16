from django.db import models
from django.contrib.auth.models import User

class CaptionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    caption = models.TextField()
    language = models.CharField(max_length=50)
    translated_text = models.TextField()
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.caption[:50]}"