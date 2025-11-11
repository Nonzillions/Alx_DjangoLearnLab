from relationship_app.models import Author, Book, Library, Librarian


# Query 1: Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return books


# Query 2: List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()


# Query 3: Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)


# Sample execution for demonstration (Uncomment if testing in Django shell)
# print(get_books_by_author("John Doe"))
# print(get_books_in_library("Central Library"))
# print(get_librarian_for_library("Central Library"))
