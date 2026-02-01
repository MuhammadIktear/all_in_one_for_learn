BookApp - Advanced Django Book Management API and System Design Concepts in Practice

A Django-based Book management application demonstrating high-performance system design concepts, including indexing, caching, async tasks with Celery, scheduled tasks with Celery Beat, request throttling, safe concurrent operations using database transactions, signals, and paginated APIs.

Features Overview

1. CRUD API for Book model (GET, POST, PATCH, DELETE)

2. Filtering & Search on multiple fields (title, author, published_date) and full-text search

3. Database Indexing on author and published_date for fast query performance

4. Pagination for GET requests to avoid overwhelming responses in high-traffic endpoints

5. Caching (Redis) for GET requests to reduce DB hits

6. Signals for logging or triggering actions when a Book is created or updated

7. Asynchronous Email using Celery worker

8. Scheduled Tasks using Celery Beat (daily and yearly emails)

9. Request Throttling (UserRateThrottle & custom TokenBucketThrottle)

10. Safe concurrent purchases using database transactions and select_for_update
