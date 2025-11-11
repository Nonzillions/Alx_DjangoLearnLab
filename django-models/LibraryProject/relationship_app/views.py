from django.shortcuts import render
from .models import Book

# Function-based view
def list_books(request):
    books = Book.objects.all()  # Get all books from database
    return render(request, 'list_books.html', {'books': books})

from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
