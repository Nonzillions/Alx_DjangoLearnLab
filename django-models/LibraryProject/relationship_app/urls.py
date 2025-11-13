from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Book views
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book_view, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book_view, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book_view, name='delete_book'),

    # Library detail
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # User authentication
    path('register/', views.register_view, name='register'),  # function-based register view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # class-based login
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # class-based logout

    # Role-based views
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
