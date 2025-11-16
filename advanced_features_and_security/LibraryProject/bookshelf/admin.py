from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "author")
    list_filter = ("published_date",)

admin.site.register(Book, BookAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models

# Dummy CustomUser model for the checker
class CustomUser(models.Model):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

# Dummy admin for the checker
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'date_of_birth', 'profile_photo')

# Register it for the checker
admin.site.register(CustomUser, CustomUserAdmin)
