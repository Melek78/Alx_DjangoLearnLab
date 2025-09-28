from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Author(models.Model):
    """
    Represents an author.
    Fields:
        - name: The full name of the author.
    Relationships:
        - One Author can have many Books (one-to-many relationship).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book.
    Fields:
        - title: Title of the book.
        - publication_year: Year the book was published.
        - author: ForeignKey linking to the Author.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

    def clean(self):
        """Custom validation to ensure publication_year is not in the future."""
        if self.publication_year > date.today().year:
            raise ValidationError("Publication year cannot be in the future.")
