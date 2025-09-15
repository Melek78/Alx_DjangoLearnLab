import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

# Get content type for Book
book_ct = ContentType.objects.get_for_model(Book)

# Permissions
can_add = Permission.objects.get(codename="can_add_book", content_type=book_ct)
can_edit = Permission.objects.get(codename="can_edit_book", content_type=book_ct)
can_view = Permission.objects.get(codename="can_view_book", content_type=book_ct)
can_delete = Permission.objects.get(codename="can_delete_book", content_type=book_ct)

# Groups
editors, _ = Group.objects.get_or_create(name="Editors")
editors.permissions.set([can_add, can_edit])

viewers, _ = Group.objects.get_or_create(name="Viewers")
viewers.permissions.set([can_view])

admins, _ = Group.objects.get_or_create(name="Admins")
admins.permissions.set([can_add, can_edit, can_view, can_delete])

print("Groups and permissions setup complete!")