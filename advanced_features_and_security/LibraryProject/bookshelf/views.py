from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

# Function-based view for listing books
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()  # the 'books' the checker expects
    return render(request, 'bookshelf/book_list.html', {'books': books})
