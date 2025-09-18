from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """
    Simple CSP header middleware. For production, consider django-csp package
    for a more complete solution.
    """
    def process_response(self, request, response):
        default_src = " ".join(settings.CSP_DEFAULT_SRC) if hasattr(settings, "CSP_DEFAULT_SRC") else "'self'"
        # Example: allow only same origin for scripts/styles/images.
        csp = (
            f"default-src {default_src}; "
            f"script-src 'self'; "
            f"style-src 'self' 'unsafe-inline'; "
            f"img-src 'self' data:; "
            f"object-src 'none'; "
            f"base-uri 'self'; "
            f"frame-ancestors 'none';"
        )
        response.setdefault("Content-Security-Policy", csp)
        return response