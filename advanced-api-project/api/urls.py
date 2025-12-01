from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints (REQUIRED by your task)
    path('books/', views.BookListView.as_view(), name='book-list'),           # ListView
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),  # DetailView
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),    # CreateView
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),  # UpdateView
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),  # DeleteView
    
    # Author endpoints (OPTIONAL - only if you want them)
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]