from django.urls import path
from . import views

urlpatterns = [
    path('audiobooks/', views.audiobook, name='audiobook'),
    path('download-books/', views.download_books, name='download_books'),
    path('audiobooks/create/', views.create_audiobook, name='create_audiobook'),
    path('edit/<int:audiobook_id>/', views.edit_audiobook, name='edit_audiobook'),
    path('delete/<int:audiobook_id>/', views.delete_audiobook, name='delete_audiobook'),
    path('download/<int:audiobook_id>/', views.download_audiobook, name='download_audiobook'),
]
