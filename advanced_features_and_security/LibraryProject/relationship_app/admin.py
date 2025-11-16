from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser  # Commented out because we moved it to bookshelf

# Comment out all old CustomUser admin code
"""
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'date_of_birth', 'is_staff'
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
"""

# Keep other admin registrations if any
