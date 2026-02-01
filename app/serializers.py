from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    book_with_author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'book_with_author_name']
        
    def get_book_with_author_name(self,obj):
        return f"{obj.title} by {obj.author}"
    
    def validate_published_date(self, value):
        import datetime
        if value > datetime.date.today():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return value