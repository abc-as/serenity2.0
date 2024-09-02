from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre
from .forms import BookForm
from django.views.generic import ListView, DetailView
from django.db.models import Q
from dashboard.models import ReadingHistory, RecentlyViewed, SaveBook
from django.contrib.auth.decorators import login_required
from .utils import synthesize_and_play_speech
from django.conf import settings
from recomendations.models import UserIntrests
import re
from haystack.query import SearchQuerySet, SQ


class BookListView(ListView):
    model = Book
    template_name = 'home.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_genre = self.request.GET.get('genre', '')
        has_audiobook = self.request.GET.get('has_audiobook', '') == 'on'

        if selected_genre:
            queryset = queryset.filter(genre__id=selected_genre)

        if has_audiobook:
            queryset = queryset.filter(audiobooks__isnull=False).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['has_audiobook'] = self.request.GET.get('has_audiobook', '') == 'on'

        if self.request.user.is_authenticated:
            recently_viewed = RecentlyViewed.objects.filter(user=self.request.user).select_related('book')
            context['read_books'] = recently_viewed

            saved_books = SaveBook.objects.filter(user=self.request.user).select_related('book')
            context['saved_books'] = saved_books

            reading_history = ReadingHistory.objects.filter(user=self.request.user).select_related('book')
            context['reading_history'] = reading_history
        return context


def sanitize_filename(filename):
    sanitized = re.sub(r'[\/:*?"<>|]', '_', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['reviews'] = self.object.reviews.filter(is_moderated=True)

        audiobooks = self.object.audiobooks.all()
        context['audiobooks'] = audiobooks

        narrators = audiobooks.values_list('narrator', flat=True).distinct()
        context['narrators'] = narrators

        selected_narrator = self.request.GET.get('narrator')
        context['selected_narrator'] = selected_narrator

        if selected_narrator:
            context['filtered_audiobooks'] = audiobooks.filter(narrator=selected_narrator)
        else:
            context['filtered_audiobooks'] = audiobooks

        if self.request.user.is_authenticated:
            context['is_saved'] = SaveBook.objects.filter(user=self.request.user, book=self.object).exists()
        else:
            context['is_saved'] = False

        if self.request.user.is_authenticated:
            RecentlyViewed.objects.get_or_create(user=self.request.user, book=self.object)

        summary_text = self.object.summary.text
        book_title = self.object.title
        audio_filename = f"{sanitize_filename(book_title)}.mp3"

        audio_file_path = synthesize_and_play_speech(summary_text, audio_filename)
        context['audio_file_url'] = settings.MEDIA_URL + 'text-to-speech/' + audio_filename

        return context

def add_or_edit_book(request, pk=None):
    if pk:
        book = get_object_or_404(Book, pk=pk)
    else:
        book = None

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'books/book_form.html', {'form': form})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


def patch_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)

    form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})


def search_books(request):
    query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')

    books = Book.objects.all()

    if query:
        UserIntrests.objects.create(user=request.user, text=query)
        sqs = SearchQuerySet().models(Book).all()
        sqs = sqs.filter(SQ(title__icontains=query) | SQ(isbn__icontains=query) | SQ(author__icontains=query) | SQ(genre__icontains=query) | SQ(summary__icontains=query) | SQ(bio__icontains=query))
        ids = []
        for sq in sqs:
            ids.append(sq.pk)
        books = books.filter(id__in=ids)
    if genre_id:
        try:
            genre = Genre.objects.get(id=genre_id)
            books = books.filter(genre=genre)
        except Genre.DoesNotExist:
            books = books.none()

    genres = Genre.objects.all()

    return render(request, 'books/search_results.html', {
        'books': books,
        'genres': genres,
        'selected_genre': genre_id,
        'search_query': query
    })


def generate_audio(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        selected_voice = request.POST.get('voice', 'en-US-Wavenet-D')
        summary_text = book.summary.text
        audio_filename = f"{book.id}_summary_{selected_voice}.mp3"
        synthesize_speech(summary_text, audio_filename, selected_voice)
    return redirect('book_detail', pk=pk)


@login_required
def save_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    SaveBook.objects.get_or_create(user=request.user, book=book)
    return redirect('book_detail', pk=book.id)  # Use pk here

@login_required
def unsave_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    saved_book = SaveBook.objects.filter(user=request.user, book=book)
    if saved_book.exists():
        saved_book.delete()
    return redirect('book_detail', pk=pk)

@login_required
def book_read(request):
    selected_genre = request.GET.get('genre', '')
    books = RecentlyViewed.objects.filter(user=request.user)
    if selected_genre:
        books = books.filter(book__genre=selected_genre)
    genres = Genre.objects.all()
    return render(request, 'books/book_read.html', {'books': books, 'genres': genres, 'selected_genre': selected_genre})

@login_required
def book_summary(request):
    selected_genre = request.GET.get('genre', '')
    books = Book.objects.all()
    if selected_genre:
        books = books.filter(genre=selected_genre)
    genres = Genre.objects.all()
    return render(request, 'books/book_summary.html', {'books': books, 'genres': genres, 'selected_genre': selected_genre})
