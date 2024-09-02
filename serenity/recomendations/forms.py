from django import forms
from .models import  UserGenre
from books.models import Genre

class UserGenreForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = UserGenre
        fields = ['genres']