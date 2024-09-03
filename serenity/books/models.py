from django.db import models
from django.db.models import Avg
from django.apps import apps
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Summary(models.Model):
    book_title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"Summary for {self.book_title}"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    summary = models.OneToOneField(Summary, on_delete=models.CASCADE, related_name='book_summary')
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        ratings = self.reviews.filter(is_moderated=True).aggregate(Avg('rating'))['rating__avg']
        return round(ratings, 1) if ratings else None

    @property
    def reviews(self):
        Review = apps.get_model('reviews', 'Review')
        rvws = Review.objects.filter(book=self, is_moderated=True)
        return rvws

