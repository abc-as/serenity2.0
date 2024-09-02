from django.urls import path
from .views import select_genres, genre_success, recomended_books

urlpatterns = [
    path('select-genres/', select_genres, name='select_genres'),
    path('genre-success/', genre_success, name='genre_success'),
    path('recomendations/', recomended_books, name='recomended_books'),
]
