from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Book description'}),
        }
