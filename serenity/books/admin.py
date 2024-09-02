from django.contrib import admin
from .models import Book, Genre, Summary, Author

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Summary)
admin.site.register(Author)


