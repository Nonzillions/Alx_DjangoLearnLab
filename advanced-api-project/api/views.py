from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    GET  → List all authors
    POST → Create a new author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    → Retrieve a single author
    PUT    → Update author
    PATCH  → Partial update
    DELETE → Remove author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    GET  → List all books
    POST → Create a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    → Retrieve one book
    PUT    → Update
    PATCH  → Partial update
    DELETE → Remove
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
