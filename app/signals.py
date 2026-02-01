from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookLog,Book
from django.contrib.auth.models import User

@receiver(post_save, sender=Book)
def book_log_on_save(sender,instance, created, **kwargs):
    print("From signals.py: Book saved signal received.")
    user = User.objects.first()  # Replace with actual user logic
    action= 'Created' if created else 'Updated'
    BookLog.objects.create(book=instance, user=user, action=action)