# from django.http import JsonResponse
# from .models import Book
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def book_view(request):
#     if request.method=='GET':
#         books = Book.objects.all()
#         data = []
        
#         for book in books:
#             data.append({
#                 'title':book.title,
#                 'author':book.author,
#                 'published_date':book.published_date,
#             })
#         return JsonResponse({
#             'data': data,
#             'message':'Successfully retrieved all books'
#             },status=200)
    
#     if request.method=='POST':
#         import json
#         body = json.loads(request.body)
#         title = body.get('title')
#         author = body.get('author')
#         published_date = body.get('published_date')
        
#         if not title or not author or not published_date:
#             return JsonResponse({
#                 'message':'Title, author, and published_date are required.'
#             },status=400)
        
#         book = Book.objects.create(
#             title=title,
#             author=author,
#             published_date=published_date
#         )
#         book.save()
#         return JsonResponse({
#             'message':'Book created successfully',
#         },status=201)
        
#     if request.method=='PATCH':
#         import json
#         body = json.loads(request.body)
        
#         book_id = body.get('id')
#         title = body.get('title')
#         author = body.get('author')
#         published_date = body.get('published_date')
        
#         try:
#             book =Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return JsonResponse({
#                 'message':'Book not found.'
#             },status=404)
#         if title:
#             book.title=title
#         if author:
#             book.author=author
#         if published_date:
#             book.published_date=published_date
#         book.save()
#         return JsonResponse({
#             'message':'Book updated successfully.'
#         },status=200)
        
#     if request.method=='DELETE':
#         import json
#         body = json.loads(request.body)
#         book_id = body.get('id')
        
#         try:
#             book =Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return JsonResponse({
#                 'message':'Book not found.'
#             },status=404)
        
#         book.delete()
#         return JsonResponse({
#             'message':'Book deleted successfully.'
#         },status=200)

from django.http import JsonResponse
from .models import Book
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from .serializers import BookSerializer
from rest_framework.decorators import api_view
# from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination
from django.db.models import Q
@csrf_exempt
@cache_page(60*2)
@api_view(['GET','POST','PATCH','DELETE'])
def book_view(request):
    if request.method=='GET':
        books = Book.objects.all()
        book_title = request.GET.get('title')
        book_author = request.GET.get('author')
        book_published_date = request.GET.get('published_date')
        search_query = request.GET.get('search')
        if book_title:
            books=books.filter(title__icontains=book_title)
        if book_author:
            books=books.filter(author__icontains=book_author)
        if book_published_date:
            books=books.filter(published_date=book_published_date)
        if search_query:
            books=books.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query)
            )
        paginator = CursorPagination()
        paginator.page_size = 2
        paginator.ordering = '-published_date'
        paginator_books = paginator.paginate_queryset(books, request)
        serializers = BookSerializer(paginator_books,many=True)
        return paginator.get_paginated_response({
            'data':serializers.data,
            'message':'Successfully retrieved all books'
        })
        
    if request.method=='POST':
        serializers=BookSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse({
                'message':'Book created successfully',
            },status=201)
        return JsonResponse({
            'errors':serializers.errors
        },status=400)
        
    if request.method=='PATCH':
        book_id = request.data.get('id')
        try:
            book= Book.objects.get(id=book_id)
            serializers=BookSerializer(book,data=request.data,partial=True)
            if serializers.is_valid():
                serializers.save()
                return JsonResponse({
                    'message': "Book Updated successfully.",
                },status=200)
                
            return JsonResponse({
                'errors':serializers.errors,
            },status=400)
        except Book.DoesNotExist:
            return JsonResponse({
                'message':'Book not found.'
            },status=404)
            
    if request.method=='DELETE':
        book_id= request.data.get('id')
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return JsonResponse({
                'message':'Book deleted successfully.'
            },status=200)
        except Book.DoesNotExist:
            return JsonResponse({
                'message':'Book not found.'
            },status=404)
            
#import atomic transaction
from django.db import transaction
from rest_framework.decorators import throttle_classes
from .tasks import send_purchase_email
from django.contrib.auth.models import User
from .throttles import PurchaseRateThrottle
@api_view(['POST'])           
@throttle_classes([PurchaseRateThrottle])
def purchase_book(request):
    user = User.objects.first()  # Replace with actual user logic
    book_id=request.data.get('book_id')
    print(f"User {user.username} is attempting to purchase book id {book_id}")
    if not book_id:
        return JsonResponse({
            'message':'book_id is required to purchase a book.'
        },status=400)
    with transaction.atomic():
        try:
            book = Book.objects.select_for_update().get(id=book_id)
            if user.userprofile.balance < book.price:
                return JsonResponse({
                    'message':'Insufficient balance to purchase the book.'
                },status=400)
            user.userprofile.balance -= book.price
            user.userprofile.save()
            print(user.email)
            send_purchase_email.delay(user.email, book.title)
            return JsonResponse({
                'message':'Book purchased successfully.'
            },status=200)
        except Book.DoesNotExist:
            return JsonResponse({
                'message':'Book not found.'
            },status=404)
    
    