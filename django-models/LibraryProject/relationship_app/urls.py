from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    # Function-based view
    path('books/', views.list_books, name='list_books'),

    # Class-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),  # function-based register view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # class-based login
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # class-based logout
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
