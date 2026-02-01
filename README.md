BookApp - Advanced Django Book Management API

A Django-based Book management application demonstrating high-performance system design concepts, including indexing, caching, async tasks with Celery, scheduled tasks with Celery Beat, request throttling, and safe concurrent operations using database transactions.

Features Overview

CRUD API for Book model (GET, POST, PATCH, DELETE)

Filtering & Search on multiple fields (title, author, published_date) and full-text search

Database Indexing on author and published_date for fast query performance

Caching (Redis) for GET requests to reduce DB hits

Asynchronous Email using Celery worker

Scheduled Tasks using Celery Beat (daily and yearly emails)

Request Throttling with built-in and custom Token Bucket algorithm

Safe concurrent purchases using database transactions and select_for_update

System Design Concepts in Practice
1. CRUD & Transactions

All endpoints (GET, POST, PATCH, DELETE) are implemented with atomic transactions where needed.

Example: Book purchase API uses transaction.atomic() and select_for_update() to safely update user balances and prevent race conditions in high-traffic scenarios:

with transaction.atomic():
    book = Book.objects.select_for_update().get(id=book_id)
    if user.userprofile.balance < book.price:
        return JsonResponse({'message':'Insufficient balance'}, status=400)
    user.userprofile.balance -= book.price
    user.userprofile.save()


This ensures that concurrent purchase requests cannot overdraw the user's balance.

2. Filtering & Search

Users can filter books by title, author, published_date, or use a full-text search query across multiple fields.

Implemented using Django ORM and Q objects:

books = Book.objects.all()
if search_query:
    books = books.filter(
        Q(title__icontains=search_query) |
        Q(author__icontains=search_query)
    )


Efficient queries are supported by database indexes on author and published_date.

3. Database Indexing

The Book model defines compound indexes:

class Meta:
    indexes = [
        models.Index(fields=['author','published_date']),
    ]


Queries on author and published_date fields are much faster because the database uses the index.

4. Caching

GET requests are cached using Redis for 5 minutes by default.

Example:

@cache_page(60 * 5)  # cache for 5 minutes
@api_view(['GET'])
def book_list(request):
    ...


Reduces DB load in high-traffic endpoints.

5. Asynchronous Emails (Celery Worker)

Sending emails is offloaded to Celery, preventing delays in API response times.

Example:

send_purchase_email.delay(user.email, book.title)


Redis acts as the message broker / queue for Celery tasks.

Celery worker continuously polls the Redis queue and executes tasks asynchronously.

6. Scheduled Tasks (Celery Beat)

Daily email summary and yearly book fair email are scheduled using Celery Beat:

app.conf.beat_schedule = {
    'daily_book_log_email': {
        'task': 'books.tasks.send_daily_book_log',
        'schedule': crontab(hour=22, minute=0),
    },
    'yearly_book_fair_email': {
        'task': 'books.tasks.send_yearly_book_fair',
        'schedule': crontab(month_of_year=2, day_of_month=1, hour=10, minute=0),
    },
}


Celery Beat pushes tasks into the Redis queue at scheduled times.

7. Request Throttling

Throttling prevents spammy requests and protects high-traffic endpoints.

Built-in throttles:

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/min',
        'user': '60/min',
    }
}


Custom Token Bucket Throttle implemented for purchase endpoint for smoother rate limiting:

class TokenBucketThrottle(UserRateThrottle):
    scope = 'purchase'


Returns a custom message with remaining time instead of HTTP 429.

8. Serializer Enhancements

The BookSerializer adds dynamic fields without modifying the database:

class BookSerializer(serializers.ModelSerializer):
    book_with_author_name = serializers.SerializerMethodField()
    
    def get_book_with_author_name(self, obj):
        return f"{obj.title} by {obj.author}"


This follows industry standard: keep extra computed fields in serializer rather than model unless needed for database queries.

9. High-Traffic Safety Features

Atomic transactions + select_for_update prevent race conditions.

Redis caching prevents repeated heavy DB queries.

Celery asynchronous processing keeps API responses fast.

Throttling prevents abuse or accidental overload.

Installation & Setup
1. Clone the repo
git clone https://github.com/MuhammadIktear/all_in_one_for_learn.git
cd bookapp

2. Create virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Configure Redis
redis-server

4. Migrate database
python manage.py migrate

5. Run Celery Worker
celery -A bookapp worker -l info

6. Run Celery Beat
celery -A bookapp beat -l info

7. Run Django Server
python manage.py runserver

Testing Endpoints

Use Postman or curl to test:

/api/books/ → CRUD, filtering, pagination, search

/api/purchase/ → purchase book with throttling and async email

Token Authentication required for user-specific endpoints.

Conclusion

BookApp demonstrates end-to-end scalable design in Django:

Database optimization (indexes, select_for_update)

High-performance API (caching, throttling)

Asynchronous background tasks (Celery)

Scheduled tasks (Celery Beat)

Industry-standard serializers for computed fields

This project can be extended to payment integration, real-time notifications, and high-concurrency applications.
