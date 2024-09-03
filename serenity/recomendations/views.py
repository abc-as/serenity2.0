from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import  UserGenre, UserIntrests
from .forms import UserGenreForm
from books.models import Genre, Book
from .utils import get_book_recommendations


@login_required(login_url='/login')
def select_genres(request):
    if request.method == 'POST':
        form = UserGenreForm(request.POST, user=request.user)
        if form.is_valid():
            UserGenre.objects.filter(user=request.user).delete()
            for genre in form.cleaned_data['genres']:
                UserGenre.objects.create(user=request.user, name=genre.name)
            return redirect('genre_success')
        else:
            return redirect('/profile')
    else:
        return HttpResponse('Invalid request!')

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