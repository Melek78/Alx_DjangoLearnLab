# Delete Book Instance

```python
from bookshelf.models import Book

book = Book.objects.get(id=1)  # retrieve the book first
book.delete()
Book.objects.all()
# <QuerySet []>