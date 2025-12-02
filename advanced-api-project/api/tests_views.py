"""
Unit Tests for Book API Endpoints
This file tests all CRUD operations, permissions, filtering, searching, and ordering.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book
from datetime import datetime

class BookAPITestCase(TestCase):
    """
    Base test case class that sets up test data and provides helper methods.
    """
    
    def setUp(self):
        """
        Set up test data before each test runs.
        Creates test users, authors, and books.
        """
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='password123',
            email='admin@example.com'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='password123',
            email='regular@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        # Create API clients
        self.client = APIClient()
        self.admin_client = APIClient()
        self.regular_client = APIClient()
        
        # Authenticate clients
        self.admin_client.force_authenticate(user=self.admin_user)
        self.regular_client.force_authenticate(user=self.regular_user)
    
    def tearDown(self):
        """
        Clean up after tests (optional - Django does this automatically)
        """
        pass

class AuthenticationTests(BookAPITestCase):
    """
    Tests for authentication and permission controls.
    """
    
    def test_unauthenticated_access_to_list(self):
        """Unauthenticated users can view book list"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_access_to_detail(self):
        """Unauthenticated users can view single book"""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_cannot_create(self):
        """Unauthenticated users cannot create books"""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_can_create(self):
        """Authenticated users can create books"""
        data = {
            'title': 'The Hobbit',
            'publication_year': 1937,
            'author': self.author1.id
        }
        response = self.admin_client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)  # 3 existing + 1 new

class CRUDOperationTests(BookAPITestCase):
    """
    Tests for Create, Read, Update, Delete operations.
    """
    
    def test_create_book(self):
        """Test creating a new book with valid data"""
        data = {
            'title': 'New Fantasy Book',
            'publication_year': 2020,
            'author': self.author2.id
        }
        response = self.admin_client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Fantasy Book')
        self.assertEqual(Book.objects.count(), 4)
    
    def test_create_book_invalid_year(self):
        """Test creating book with future publication year (should fail)"""
        future_year = datetime.now().year + 1
        data = {
            'title': 'Book from Future',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.admin_client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_retrieve_book_list(self):
        """Test retrieving list of all books"""
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should have 3 books
    
    def test_retrieve_single_book(self):
        """Test retrieving a single book by ID"""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_update_book(self):
        """Test updating an existing book"""
        updated_data = {
            'title': 'Updated Title',
            'publication_year': 2000,
            'author': self.author1.id
        }
        response = self.admin_client.put(
            f'/api/books/{self.book1.id}/update/',
            updated_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()  # Refresh from database
        self.assertEqual(self.book1.title, 'Updated Title')
    
    def test_delete_book(self):
        """Test deleting a book"""
        initial_count = Book.objects.count()
        response = self.admin_client.delete(f'/api/books/{self.book1.id}/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

class FilterSearchOrderTests(BookAPITestCase):
    """
    Tests for filtering, searching, and ordering functionality.
    """
    
    def test_filter_by_author(self):
        """Test filtering books by author"""
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return 2 books by author1
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year"""
        response = self.client.get(f'/api/books/?publication_year=1997')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book1.title)
    
    def test_search_by_title(self):
        """Test searching books by title keyword"""
        response = self.client.get('/api/books/?search=Harry')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
    
    def test_search_by_author_name(self):
        """Test searching books by author name"""
        response = self.client.get('/api/books/?search=Martin')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book3.title)
    
    def test_ordering_by_title_asc(self):
        """Test ordering books by title (A-Z)"""
        response = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # Should be sorted alphabetically
    
    def test_ordering_by_title_desc(self):
        """Test ordering books by title (Z-A)"""
        response = self.client.get('/api/books/?ordering=-title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))  # Reverse alphabetical
    
    def test_ordering_by_year_desc(self):
        """Test ordering books by publication year (newest first)"""
        response = self.client.get('/api/books/?ordering=-publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))  # Descending years
    
    def test_combined_filter_search_order(self):
        """Test combined filtering, searching, and ordering"""
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&search=Harry&ordering=-publication_year'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should get Harry Potter books by author1, newest first
        self.assertEqual(len(response.data), 2)
        self.assertTrue(response.data[0]['publication_year'] >= response.data[1]['publication_year'])

class ValidationTests(BookAPITestCase):
    """
    Tests for data validation rules.
    """
    
    def test_publication_year_cannot_be_future_on_create(self):
        """Test that publication year cannot be in the future when creating"""
        future_year = datetime.now().year + 5
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.admin_client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertIn('Cannot be in the future', str(response.data))
    
    def test_publication_year_cannot_be_future_on_update(self):
        """Test that publication year cannot be in the future when updating"""
        future_year = datetime.now().year + 3
        data = {
            'title': 'Updated Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.admin_client.put(
            f'/api/books/{self.book1.id}/update/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

class EdgeCaseTests(BookAPITestCase):
    """
    Tests for edge cases and error handling.
    """
    
    def test_get_nonexistent_book(self):
        """Test retrieving a book that doesn't exist"""
        response = self.client.get('/api/books/999/')  # Non-existent ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_book(self):
        """Test updating a book that doesn't exist"""
        data = {'title': 'Updated', 'publication_year': 2020, 'author': self.author1.id}
        response = self.admin_client.put('/api/books/999/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist"""
        response = self.admin_client.delete('/api/books/999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_missing_required_fields_on_create(self):
        """Test creating book with missing required fields"""
        data = {'title': 'Incomplete Book'}  # Missing publication_year and author
        response = self.admin_client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)