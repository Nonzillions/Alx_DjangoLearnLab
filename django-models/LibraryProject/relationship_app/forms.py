from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    # Customize published_date to use a date picker
    published_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']
