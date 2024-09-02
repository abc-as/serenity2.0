from django import forms
from .models import Audiobook

class AudiobookForm(forms.ModelForm):
    class Meta:
        model = Audiobook
        fields = ['book', 'audio_file', 'duration', 'is_available']


class AudiobookCreateForm(forms.ModelForm):
    class Meta:
        model = Audiobook
        fields = ['book', 'audio_file', 'duration','narrator', 'is_available']

