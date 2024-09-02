from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import  UserGenre, UserIntrests
from .forms import UserGenreForm
from books.models import Genre, Book
from django.db.models import Q
from .utils import get_book_recommendations
import openai
from haystack.query import SearchQuerySet, SQ


@login_required
def select_genres(request):
    if request.method == 'POST':
        form = UserGenreForm(request.POST)
        if form.is_valid():
            UserGenre.objects.filter(user=request.user).delete()
            for genre in form.cleaned_data['genres']:
                UserGenre.objects.create(user=request.user, name=genre.name)
            return redirect('genre_success')
    else:
        form = UserGenreForm()

    return render(request, 'recomendations/gener_select.html', {'form': form})


def genre_success(request):
    return render(request, 'recomendations/genre_success.html')



@login_required
def recomended_books(request):
    user = request.user
    user_interests = UserIntrests.objects.filter(user=user)
    user_genres = UserGenre.objects.filter(user=user)

    recommendations = get_book_recommendations(user_interests, user_genres)

    books_by_genre = {}
    for genre, book_titles in recommendations.items():
        books = Book.objects.filter(genre__name=genre)
        if books.exists():
            books_by_genre[genre] = list(books)
        
    genres = Genre.objects.all()

    return render(request, 'recomendations/recomended_books.html', {
        'books_by_genre': books_by_genre,
        'genres': genres,
        'selected_genre': request.GET.get('genre', ''),
    })