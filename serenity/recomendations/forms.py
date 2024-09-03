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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            selected_genres = UserGenre.objects.filter(user=user).values_list('name', flat=True)
            self.fields['genres'].initial = Genre.objects.filter(name__in=selected_genres)
