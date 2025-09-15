from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # include all fields you want in the form
        fields = ['title', 'author', 'published_date']