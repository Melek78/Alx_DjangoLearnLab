import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Variables for queries
author_name = "J.K. Rowling"
library_name = "Central Library"

def run_queries():
    # 1. Query all books by a specific author
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = author.books.all()
        print(f"Books by {author.name}:")
        for book in books_by_author:
            print("-", book.title)
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")

    print("\n" + "-"*40 + "\n")

    # 2. List all books in a library
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"Books in {library.name}:")
        for book in books_in_library:
            print("-", book.title)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

    print("\n" + "-"*40 + "\n")

    # 3. Retrieve the librarian for a library
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        print(f"Librarian of {library.name}: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print(f"Library or Librarian for '{library_name}' not found.")

if __name__ == "__main__":
    run_queries()
