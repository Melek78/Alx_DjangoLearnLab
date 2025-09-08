import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():

    try:
        author = Author.objects.get(name="J.K. Rowling")
        books_by_author = author.books.all()
        print(f"Books by {author.name}:")
        for book in books_by_author:
            print("-", book.title)
    except Author.DoesNotExist:
        print("Author not found.")

    print("\n" + "-"*40 + "\n")

    try:
        library = Library.objects.get(name="Central Library")
        books_in_library = library.books.all()
        print(f"Books in {library.name}:")
        for book in books_in_library:
            print("-", book.title)
    except Library.DoesNotExist:
        print("Library not found.")

    print("\n" + "-"*40 + "\n")

    try:
        library = Library.objects.get(name="Central Library")
        librarian = library.librarian
        print(f"Librarian of {library.name}: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print("Library or Librarian not found.")


if __name__ == "__main__":
    run_queries()
