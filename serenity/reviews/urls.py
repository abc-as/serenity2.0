from django.urls import path
from . import views

urlpatterns = [
    path('review/submit/<int:book_id>/', views.submit_review, name='submit_review'),
    path('review/moderate/<int:review_id>/', views.moderate_review, name='moderate_review'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback/thanks/', views.feedback_thanks, name='feedback_thanks'),
    path('contact/', views.contactUs, name='contact'),
]
