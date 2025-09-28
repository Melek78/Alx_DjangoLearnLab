# Book API (Beginner Version)

These are the endpoints for my Book API. I made it to practice Django REST Framework.

- `/api/books/` (GET) → Shows all books. Everyone can see.
- `/api/books/<id>/` (GET) → Shows one book by its ID. Everyone can see.
- `/api/books/create/` (POST) → Make a new book. You have to be logged in.
- `/api/books/<id>/update/` (PUT or PATCH) → Change a book. Only logged in users.
- `/api/books/<id>/delete/` (DELETE) → Remove a book. Only logged in users.

I used `permission_classes` to control who can do what.  
I also added `perform_create` and `perform_update` hooks in case I want to do extra stuff later.  
Right now they just save the book normally.
