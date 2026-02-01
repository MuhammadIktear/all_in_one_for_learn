from django.urls import path,include
from .views import book_view, purchase_book

urlpatterns = [
    path('books/',book_view),
    path('purchase/',purchase_book)
]
