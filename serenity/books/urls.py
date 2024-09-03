from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/add/', views.add_or_edit_book, name='add_book'),
    path('book/edit/<int:pk>/', views.add_or_edit_book, name='edit_book'),
    path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('book/patch/<int:pk>/', views.patch_book, name='patch_book'),
    path('search/', views.search_books, name='search_books'),  # Add search_books view
    path('generate_audio/<int:pk>/', views.generate_audio, name='generate_summary_audio'),
    path('book/<int:pk>/save/', views.save_book, name='save_book'),
    path('unsave-book/<int:pk>/', views.unsave_book, name='unsave_book'),
    path('book-read/', views.book_read, name='book_read'),
    path('book-summary/', views.book_summary, name='book_summary'),
]
