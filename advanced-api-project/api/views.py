# CORRECT IMPORTS - DO THIS EXACTLY
from rest_framework import generics, serializers, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from django_filters.rest_framework import DjangoFilterBackend  # Add this import

class AuthorListCreateView(generics.ListCreateAPIView):
    """List and create authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookGenericUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView without specific ID
    Usually handles via request data or different logic
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        book_id = self.request.data.get('id')
        if book_id:
            return Book.objects.get(id=book_id)
        return Book.objects.first()

class BookGenericDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView without specific ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        book_id = self.request.data.get('id')
        if book_id:
            return Book.objects.get(id=book_id)
        return Book.objects.first()

# 1. LIST VIEW - Shows all books WITH FILTERING, SEARCHING, ORDERING
class BookListView(generics.ListAPIView):
    """
    ListView: Retrieves all books from the database with advanced query capabilities.
    URL: GET /api/books/
    
    FILTERING: Use query parameters to filter results
    - ?author=1                     Filter by author ID
    - ?publication_year=2023        Filter by exact year
    - ?title=Specific Title         Filter by exact title
    
    SEARCHING: Search across multiple fields
    - ?search=django                Search in title or author name (case-insensitive)
    - ?search=python                Returns books with 'python' in title or author name
    
    ORDERING: Sort results by any field
    - ?ordering=title               A-Z by title
    - ?ordering=-publication_year   Newest books first (descending)
    - ?ordering=author              Order by author ID
    
    COMBINED EXAMPLES:
    - ?author=1&ordering=-publication_year  Author's books, newest first
    - ?search=web&ordering=title            Web-related books, alphabetical
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Step 1, 2, 3: Add filtering, searching, and ordering backends
    filter_backends = [
        DjangoFilterBackend,      # For field-based filtering
        filters.SearchFilter,     # For text search across fields
        filters.OrderingFilter,   # For sorting results
    ]
    
    # Step 1: Filtering setup - which fields can be filtered
    filterset_fields = [
        'author',           # Foreign key field: filter by author ID
        'publication_year', # Integer field: filter by exact year
        'title',            # Char field: filter by exact title match
    ]
    
    # Step 2: Searching setup - which fields are searchable
    search_fields = [
        'title',            # Search in book titles
        'author__name',     # Search in author names (through foreign key relationship)
    ]
    
    # Step 3: Ordering setup - which fields can be used for sorting
    ordering_fields = [
        'title',            # Sort alphabetically by book title
        'publication_year', # Sort by publication year (ascending/descending)
        'author',           # Sort by author ID
        'author__name',     # Sort alphabetically by author name
    ]
    
    # Default ordering if no ordering parameter is provided
    ordering = ['title']  # Default: books ordered alphabetically by title

# 2. DETAIL VIEW - Shows one specific book
class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView: Retrieves a single book by its ID.
    URL: GET /api/books/<id>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# 3. CREATE VIEW - Adds a new book
class BookCreateView(generics.CreateAPIView):
    """
    CreateView: Adds a new book to the database.
    URL: POST /api/books/create/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        publication_year = serializer.validated_data.get('publication_year')
        current_year = datetime.now().year
        
        if publication_year > current_year:
            raise serializers.ValidationError(
                {"publication_year": "Cannot be in the future."}
            )
        
        serializer.save()

# 4. UPDATE VIEW - Modifies an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Modifies an existing book.
    URL: PUT /api/books/<id>/update/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        publication_year = serializer.validated_data.get('publication_year')
        current_year = datetime.now().year
        
        if publication_year and publication_year > current_year:
            raise serializers.ValidationError(
                {"publication_year": "Cannot be in the future."}
            )
        
        serializer.save()

# 5. DELETE VIEW - Removes a book
class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Removes a book from the database.
    URL: DELETE /api/books/<id>/delete/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]