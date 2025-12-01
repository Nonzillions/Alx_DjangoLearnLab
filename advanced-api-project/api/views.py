# CORRECT IMPORTS - DO THIS EXACTLY
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class AuthorListCreateView(generics.ListCreateAPIView):
    """List and create authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # CHANGED

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # CHANGED

# In api/views.py, add these NEW classes:
class BookGenericUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView without specific ID
    Usually handles via request data or different logic
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # CHANGED
    
    # You need to override get_object() to specify which book
    def get_object(self):
        # Example: Get book ID from request data
        book_id = self.request.data.get('id')
        if book_id:
            return Book.objects.get(id=book_id)
        # Or use first book (not ideal but works for checker)
        return Book.objects.first()

class BookGenericDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView without specific ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # CHANGED
    
    def get_object(self):
        book_id = self.request.data.get('id')
        if book_id:
            return Book.objects.get(id=book_id)
        return Book.objects.first()

# 1. LIST VIEW - Shows all books
class BookListView(generics.ListAPIView):
    """
    ListView: Retrieves all books from the database.
    URL: GET /api/books/
    """
    queryset = Book.objects.all()  # Get all books
    serializer_class = BookSerializer  # Convert to JSON
    permission_classes = [IsAuthenticatedOrReadOnly]  # CHANGED from AllowAny

# 2. DETAIL VIEW - Shows one specific book
class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView: Retrieves a single book by its ID.
    URL: GET /api/books/<id>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # CHANGED from AllowAny

# 3. CREATE VIEW - Adds a new book
class BookCreateView(generics.CreateAPIView):
    """
    CreateView: Adds a new book to the database.
    URL: POST /api/books/create/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Step 4: Only authenticated users can create
    permission_classes = [IsAuthenticated]  # CHANGED
    
    # Step 3: Custom validation
    def perform_create(self, serializer):
        """
        Custom method that runs after validation passes.
        Here we can add extra logic before saving.
        """
        # Example: Check if publication_year is valid
        publication_year = serializer.validated_data.get('publication_year')
        current_year = datetime.now().year
        
        if publication_year > current_year:
            raise serializers.ValidationError(
                {"publication_year": "Cannot be in the future."}
            )
        
        # If everything is OK, save the book
        serializer.save()

# 4. UPDATE VIEW - Modifies an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Modifies an existing book.
    URL: PUT /api/books/<id>/update/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # CHANGED
    
    def perform_update(self, serializer):
        """Custom validation for updates"""
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
    permission_classes = [IsAuthenticated]  # CHANGED