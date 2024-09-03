from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ReadingHistory
from books.models import Book

@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    saved_books = user.saved_books.all()
    reading_history = user.reading_history.all()

    # Assuming you want to provide book recommendations, you can fetch them here
    recommendations = Book.objects.exclude(id__in=saved_books.values_list('book_id', flat=True)).order_by('?')[:5]

    context = {
        'saved_books': saved_books,
        'reading_history': reading_history,
        'recommendations': recommendations,
    }
    return render(request, 'dashboard/dashboard.html', context)
