# Security hardening notes

## What I changed
- `settings.py`
  - Set secure cookie flags: `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`.
  - Browser protections: `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF`.
  - HSTS and SSL redirect settings included (enable only on real HTTPS deployment).
- CSP header
  - Added `LibraryProject/middleware.py` with `Content-Security-Policy` header.
  - Added the middleware to `MIDDLEWARE`.
- Templates
  - All forms include `{% csrf_token %}`. Example in `bookshelf/templates/...`.
- Views & Forms
  - Added `bookshelf/forms.py` to validate user input (e.g., search).
  - Views updated to use Django ORM and forms (prevents SQL injection and enforces validation).
- Permissions
  - Views use `@permission_required(..., raise_exception=True)` so unauthorized users receive 403.

## Manual tests
1. CSRF:
   - Submit a form without the CSRF token — Django should block it (HTTP 403).
2. XSS:
   - Try to submit a book title with `<script>` — Django templates escape output and CSP header blocks inline scripts.
3. SQL injection:
   - Try to put `' OR 1=1; --` into search input — ORM `filter(title__icontains=...)` treats it as a normal string.
4. CSP header:
   - Inspect response headers in browser devtools → should see `Content-Security-Policy`.

## Production checklist
- Serve site over HTTPS.
- Set `DEBUG = False`.
- Update `ALLOWED_HOSTS` with your real hostnames.
- Ensure `SECRET_KEY` is kept secret and not in source control.
- Consider using the `django-csp` package for robust CSP management.

