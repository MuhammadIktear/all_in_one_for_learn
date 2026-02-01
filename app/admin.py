from django.contrib import admin
from .models import Book, UserProfile, BookLog
admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(BookLog)
# Register your models here.
