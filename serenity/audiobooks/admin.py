from django.contrib import admin
from .models import Audiobook, Download

@admin.register(Audiobook)
class AudiobookAdmin(admin.ModelAdmin):
    list_display = ('book', 'audio_file', 'duration', 'is_available', 'narrator', 'created_at')
    search_fields = ('book__title', 'narrator')
@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'audiobook', 'downloaded_at')
