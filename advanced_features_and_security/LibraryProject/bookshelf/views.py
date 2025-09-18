from django.shortcuts import render, get_list_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import SearchForm
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            # safe ORM filter (parameterized): no string-formatting
            books = books.filter(title__icontains=q)

    context = {"books": books, "form": form}
    return render(request, "bookshelf/book_list.html", context)


# Create view example: uses POST + permission + Django form (not shown)
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == "POST":
        # use a Django ModelForm in real app for validation.
        title = request.POST.get("title", "").strip()
        author_id = request.POST.get("author")  # validate this carefully in real code
        if not title:
            return render(request, "bookshelf/book_form.html", {"error": "Title is required."})
        Book.objects.create(title=title)  # keep logic minimal here; prefer ModelForm
        return redirect("bookshelf:book_list")
    return render(request, "bookshelf/book_form.html")
