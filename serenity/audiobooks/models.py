from django.db import models
from books.models import Book
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Audiobook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='audiobooks')
    audio_file = models.FileField(upload_to='audiobooks/')
    duration = models.DurationField()  # Duration of the audiobook
    is_available = models.BooleanField(default=True)  # To indicate if the audiobook is available
    created_at = models.DateTimeField(auto_now_add=True)
    narrator = models.CharField(_('narrator'), max_length=255, blank=True, null=True)


    def __str__(self):
        return f"Audiobook for {self.book.title}"


class Download(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    audiobook = models.ForeignKey(Audiobook, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} downloaded {self.audiobook.book.title} at {self.downloaded_at}"
