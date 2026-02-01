BookApp - Advanced Django Book Management API and System Design Concepts in Practice

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
