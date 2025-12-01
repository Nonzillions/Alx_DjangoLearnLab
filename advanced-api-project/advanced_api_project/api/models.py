from django.db import models

# Author model — an author can have many books
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Book model — each book belongs to one author
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
