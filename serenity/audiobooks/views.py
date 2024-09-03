from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Audiobook, Download
from .forms import AudiobookForm, AudiobookCreateForm
from books.models import Book, Genre

@login_required(login_url='/login')
def download_audiobook(request, audiobook_id):
    audiobook = get_object_or_404(Audiobook, id=audiobook_id)
    # Track download in the database
    print('++++++++++++++==')
    Download.objects.create(user=request.user, audiobook=audiobook)
    # Redirect to the audio file URL
    return redirect(audiobook.audio_file.url)

@login_required(login_url='/login')
def edit_audiobook(request, audiobook_id):
    audiobook = get_object_or_404(Audiobook, id=audiobook_id)
    if not request.user.is_superuser:
        return redirect('book_list')  # Only allow admins to edit

    if request.method == 'POST':
        form = AudiobookForm(request.POST, request.FILES, instance=audiobook)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=audiobook.book.id)
    else:
        form = AudiobookForm(instance=audiobook)
    return render(request, 'audiobooks/edit_audiobook.html', {'form': form, 'audiobook': audiobook})

@login_required(login_url='/login')
def delete_audiobook(request, audiobook_id):
    audiobook = get_object_or_404(Audiobook, id=audiobook_id)
    if not request.user.is_superuser:
        return redirect('book_list')  # Only allow admins to delete

    if request.method == 'POST':
        audiobook.delete()
        return redirect('book_detail', pk=audiobook.book.id)

    return render(request, 'audiobooks/delete_audiobook.html', {'audiobook': audiobook})

@login_required(login_url='/login')
def create_audiobook(request):
    if not request.user.is_superuser:
        return redirect('book_list')  # Only allow admins to create new audiobooks

    if request.method == 'POST':
        form = AudiobookCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to book list or another page as needed
    else:
        form = AudiobookCreateForm()

    return render(request, 'audiobooks/create_audiobook.html', {'form': form})

@login_required(login_url='/login')
def audiobook(request):
    selected_genre = request.GET.get('genre', '')
    books = list(Book.objects.all().values_list('id', flat=True))
    audiobooks = Audiobook.objects.filter(book__id__in=books)
    filtered_audiobooks = []
    if selected_genre:
        audiobooks = audiobooks.filter(book__genre=selected_genre)
    audiobooks_id = []
    for book in audiobooks:
        if book.book.id not in audiobooks_id:
            filtered_audiobooks.append(book)
            audiobooks_id.append(book.book.id)

    genres = Genre.objects.all()
    return render(request, 'audiobooks/audiobooks.html', {'books': filtered_audiobooks, 'selected_genre': selected_genre, 'genres': genres})

@login_required(login_url='/login')
def download_books(request):
    selected_genre = request.GET.get('genre', '')
    books = list(Book.objects.all().values_list('id', flat=True))
    downloadbooks = Download.objects.filter(audiobook__book__id__in=books)
    filtered_audiobooks = []
    if selected_genre:
        downloadbooks = downloadbooks.filter(audiobook__book__genre=selected_genre)
    audiobooks_id = []
    for book in downloadbooks:
        if book.audiobook.book.id not in audiobooks_id:
            filtered_audiobooks.append(book)
            audiobooks_id.append(book.audiobook.book.id)

    genres = Genre.objects.all()
    return render(request, 'books/download_books.html', {'books': filtered_audiobooks, 'selected_genre': selected_genre, 'genres': genres})
