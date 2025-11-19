from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm
from .forms import ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    form = BookForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            Book.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"]
            )
            return redirect('book_list')

    return render(request, 'bookshelf/book_form.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    form = BookForm(request.POST or None, initial={
        'title': book.title,
        'description': book.description
    })

    if request.method == "POST":
        if form.is_valid():
            book.title = form.cleaned_data["title"]
            book.description = form.cleaned_data["description"]
            book.save()
            return redirect('book_list')

    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book
    })


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')
