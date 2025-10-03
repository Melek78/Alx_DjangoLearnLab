Blog Post Management (CRUD)
---------------------------
Location:
- Models: blog/models.py
- Forms: blog/forms.py
- Views: blog/views.py
- URLs: blog/urls.py (include in root urls)
- Templates: blog/templates/blog/

Usage:
- /posts/             : List all posts
- /posts/new/         : Create a new post (login required)
- /posts/<pk>/        : View a post
- /posts/<pk>/edit/   : Edit (author only)
- /posts/<pk>/delete/ : Delete (author only)

Permissions:
- Creating posts requires authentication.
- Editing/deleting require that request.user == post.author.

Notes:
- Author is automatically assigned in PostCreateView via form_valid().
- Use LoginRequiredMixin and UserPassesTestMixin for access control.
