from django.contrib import admin
from .models import RecentlyViewed, ReadingHistory, SaveBook
# Register your models here.
admin.site.register(ReadingHistory)
admin.site.register(RecentlyViewed)
admin.site.register(SaveBook)
