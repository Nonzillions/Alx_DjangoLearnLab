# api/serializers.py

from rest_framework import serializers
from .models import Author, Book
import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model fields and enforces validation.

    - Converts Book model instances to plain data (for JSON responses).
    - Converts incoming JSON into Book fields when creating/updating.
    - validate_publication_year ensures the year isn't in the future.
    """

    class Meta:
        # Tell DRF which model and which fields to include in serialized output
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Field-level validation for 'publication_year'.
        DRF automatically calls this when deserializing incoming data.
        """
        current_year = datetime.date.today().year
        if value > current_year:
            # Raise a ValidationError to stop bad data from being saved
            raise serializers.ValidationError(
                'Publication year cannot be in the future.'
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author model and nests related books.

    - The `books` field uses the related_name='books' defined on Book.author.
    - many=True because an author can have multiple books.
    - read_only=True because, in this simple example, we only display nested books.
      (If you want to create books while creating an author, you need writable nested logic.)
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
