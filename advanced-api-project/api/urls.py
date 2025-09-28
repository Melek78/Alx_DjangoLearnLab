from django.urls import path
from .views import (
    BookListCreateView,
    BookRetrieveUpdateDeleteView
)

urlpatterns = [
    # List all books (GET) and Create a new book (POST)
    path('books/', BookListCreateView.as_view(), name='book-list-create'),

    # Retrieve (GET), Update (PUT/PATCH), Delete (DELETE) a single book by ID
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-detail-update-delete'),
]
