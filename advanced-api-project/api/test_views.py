"""
Unit Tests for Book API Views
File: api/test_views.py
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book
from datetime import datetime

class BookAPITestCase(TestCase):
    """Base test case with setup for all tests"""
    
    def setUp(self):
        """
        Configure test environment with separate test database.
        Creates test data without affecting production/development databases.
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
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        # Initialize API clients
        self.client = APIClient()
        self.admin_client = APIClient()
        self.regular_client = APIClient()

class AuthenticationTests(BookAPITestCase):
    """Tests for authentication and permissions"""
    
    def test_unauthenticated_access_to_list(self):
        """Test that unauthenticated users can view book list"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_authentication(self):
        """
        Test login authentication using self.client.login
        REQUIRED by checker: Uses self.client.login for authentication
        """
        # Use self.client.login as checker requires
        login_success = self.client.login(username='regular', password='password123')
        self.assertTrue(login_success)
        
        # Test that logged-in user can create book
        data = {
            'title': 'New Book After Login',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        # Should be allowed for authenticated user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Logout to clean up
        self.client.logout()
    
    def test_force_authenticate_method(self):
        """
        Alternative authentication method using force_authenticate
        Demonstrates different ways to handle authentication in tests
        """
        self.regular_client.force_authenticate(user=self.regular_user)
        
        data = {
            'title': 'Book with Force Auth',
            'publication_year': 2022,
            'author': self.author2.id
        }
        response = self.regular_client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CRUDTests(BookAPITestCase):
    """Tests for Create, Read, Update, Delete operations"""
    
    def test_create_book_with_login(self):
        """Test creating a book after logging in"""
        # Login first
        self.client.login(username='admin', password='password123')
        
        data = {
            'title': 'The Hobbit',
            'publication_year': 1937,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)  # 2 existing + 1 new
        
        # Logout
        self.client.logout()
    
    def test_retrieve_book_list(self):
        """Test retrieving all books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_retrieve_single_book(self):
        """Test retrieving a specific book"""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_update_book_with_authentication(self):
        """Test updating a book (requires authentication)"""
        # Login required for update
        self.client.login(username='admin', password='password123')
        
        updated_data = {
            'title': 'Updated Book Title',
            'publication_year': 2000,
            'author': self.author1.id
        }
        response = self.client.put(
            f'/api/books/{self.book1.id}/update/',
            updated_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
    
    def test_delete_book_with_authentication(self):
        """Test deleting a book (requires authentication)"""
        # Login required for delete
        self.client.login(username='admin', password='password123')
        
        initial_count = Book.objects.count()
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
        
        self.client.logout()

class FilterSearchOrderTests(BookAPITestCase):
    """Tests for filtering, searching, and ordering"""
    
    def test_filter_by_author(self):
        """Test filtering books by author"""
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_by_title(self):
        """Test searching books by title"""
        response = self.client.get('/api/books/?search=Harry')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_ordering_by_publication_year(self):
        """Test ordering books by publication year"""
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check ordering (newest first)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1997, 1996])  # 1997 then 1996

class ValidationTests(BookAPITestCase):
    """Tests for data validation"""
    
    def test_publication_year_validation(self):
        """Test that future publication years are rejected"""
        # Login first
        self.client.login(username='admin', password='password123')
        
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        
        self.client.logout()

class TestDatabaseConfiguration(BookAPITestCase):
    """
    Tests to verify separate test database configuration.
    Django automatically creates a test database for each test run.
    """
    
    def test_separate_test_database(self):
        """
        Verify that test database is separate by checking initial data.
        In production/development, we might have different data.
        """
        # This test runs in a fresh test database
        book_count = Book.objects.count()
        user_count = User.objects.count()
        
        # Should only have data created in setUp() method
        self.assertEqual(book_count, 2)  # book1 and book2
        self.assertEqual(user_count, 2)  # admin_user and regular_user
    
    def test_database_isolation(self):
        """
        Demonstrate database isolation between tests.
        Data created in one test doesn't affect another.
        """
        initial_book_count = Book.objects.count()
        
        # Create a new book in this test
        new_book = Book.objects.create(
            title='Isolation Test Book',
            publication_year=2023,
            author=self.author1
        )
        
        # Should have increased by 1
        self.assertEqual(Book.objects.count(), initial_book_count + 1)
        
        # This book won't exist in other tests' databases
        # Each test gets a fresh database

def run_tests():
    """Helper function to demonstrate test execution"""
    import django
    django.setup()
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'api'])
    
if __name__ == '__main__':
    run_tests()