from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm, FeedbackForm, ContactForm
from books.models import Book
from django.contrib import messages

@login_required
def submit_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.is_moderated = True
            review.save()
            return redirect('book_detail', pk=book_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form, 'book': book})

@login_required
def moderate_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if not request.user.is_superuser:
        return redirect('book_list')  # Only allow admins to moderate
    if request.method == 'POST':
        if 'delete' in request.POST:
            review.delete()
        elif 'edit' in request.POST:
            # Implement edit functionality if needed
            pass
        return redirect('book_list')
    return render(request, 'reviews/moderate_review.html', {'review': review})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.filter(is_moderated=True).order_by('-created_at')
    return render(request, 'books/book_detail.html', {'book': book, 'reviews': reviews})



def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_thanks')  # Redirect to a thank-you page or feedback list
    else:
        form = FeedbackForm()
    return render(request, 'reviews/submit_feedback.html', {'form': form})


def feedback_thanks(request):
    return render(request, 'reviews/feedback_thanks.html')

def contactUs(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
