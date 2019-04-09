from flask import Response
from flask_wtf.csrf import generate_csrf

from auslib.web.admin.views.base import AdminView

__all__ = ["CSRFView"]


def get_csrf_headers():
    # Instantiating a Form makes sure there's a CSRF token available
    # Generate a CSRF token put an hmac key in the session.
    return {"X-CSRF-Token": generate_csrf()}


class CSRFView(AdminView):
    """/csrf_token"""

    def get(self):
        return Response(headers=get_csrf_headers())
