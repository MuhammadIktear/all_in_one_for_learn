from celery import shared_task
from django.core.mail import send_mail
@shared_task
def send_purchase_email(user_email, book_title):
    print(f"Worker: Sending email to {user_email} for {book_title}")
    send_mail(
        subject=f'Book Purchase: {book_title}',
        message=f'You purchased {book_title}.',
        from_email='iktear500@gmail.com',
        recipient_list=[user_email],
    )
    return True

from .models import BookLog
from django.utils import timezone
@shared_task
def send_daily_book_logs():
    today = timezone.localdate()
    logs = BookLog.objects.filter(timestamp__date=today)
    if not logs.exists():
        print("No book logs for today.")
        return "No logs"
    
    message=""
    for log in logs:
        message += f"{log.timestamp.strftime('%H:%M')} - {log.user.username} {log.action} '{log.book.title}'\n"
    send_mail(
        subject='Daily Book Logs',
        message=message,
        from_email='iktear500@gmail.com',
        recipient_list=['iktear500@gmail.com'],
    )
    return True

