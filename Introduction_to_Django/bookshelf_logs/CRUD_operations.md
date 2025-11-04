### Create Book

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book

### Retrieve Book
Book.objects.all()

### Update Book
book.title = "Nineteen Eighty-Four"
book.save()
book

### Delete Book
book.delete()
Book.objects.all()


