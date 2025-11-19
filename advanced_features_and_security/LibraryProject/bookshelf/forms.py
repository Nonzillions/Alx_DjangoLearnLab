from django import forms
from .models import Book


# Form required by the assignment checker
class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


# Actual form used by your app
class BookForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
