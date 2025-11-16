from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# -------------------------------
# CUSTOM USER MANAGER
# -------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)

# -------------------------------
# CUSTOM USER MODEL
# -------------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.username

# -------------------------------
# BOOK MODEL
# -------------------------------
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
