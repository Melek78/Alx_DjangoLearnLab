from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # Create a test author
        self.author = Author.objects.create(name="John Doe")

        # Create sample books
        self.book1 = Book.objects.create(
            title="Python Basics",
            author=self.author,
            publication_year=2021
        )
        self.book2 = Book.objects.create(
            title="Advanced Python",
            author=self.author,
            publication_year=2022
        )

    # ---------- CREATE ----------
    def test_create_book(self):
        url = reverse('book-create')
        data = {
            "title": "Django REST Framework",
            "author": self.author.id,
            "publication_year": 2023
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title="Django REST Framework").publication_year, 2023)

    # ---------- READ ----------
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book_detail(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # ---------- UPDATE ----------
    def test_update_book(self):
        url = reverse('book-update', args=[self.book1.id])
        data = {"title": "Python Basics Updated"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Python Basics Updated")

    # ---------- DELETE ----------
    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ---------- FILTERING ----------
    def test_filter_books_by_author(self):
        url = reverse('book-list') + f"?author={self.author.id}"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(book['author'] == self.author.id for book in response.data))

    # ---------- SEARCH ----------
    def test_search_books_by_title(self):
        url = reverse('book-list') + "?search=Advanced"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Advanced Python")

    # ---------- ORDERING ----------
    def test_order_books_by_publication_year_desc(self):
        url = reverse('book-list') + "?ordering=-publication_year"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2022)

    # ---------- PERMISSIONS ----------
    def test_unauthenticated_create_book(self):
        self.client.logout()
        url = reverse('book-create')
        data = {"title": "Unauthorized Book", "author": self.author.id, "publication_year": 2025}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
