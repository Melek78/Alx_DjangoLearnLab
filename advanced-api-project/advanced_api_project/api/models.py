from django.db import models

class Author(models.Model):
    """
    Author model represents a writer.
    Fields:
        - name: Stores the name of the author.
    Relationships:
        - One-to-Many with Book (an author can have multiple books).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a published book.
    Fields:
        - title: Title of the book.
        - publication_year: Year the book was published.
        - author: ForeignKey linking to Author.
                  Establishes a one-to-many relationship
                  (an author can have many books).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title} ({self.publication_year})"