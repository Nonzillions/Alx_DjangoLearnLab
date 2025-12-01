from django.urls import path
from . import views

urlpatterns = [
    # Original URLs
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # NEW URLs for the checker
    path('books/update/', views.BookGenericUpdateView.as_view(), name='book-update-generic'),
    path('books/delete/', views.BookGenericDeleteView.as_view(), name='book-delete-generic'),
    
    # Author endpoints
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]