from flask import Response
from flask_wtf import Form

from auslib.web.admin.views.base import AdminView

__all__ = ["CSRFView"]


def get_csrf_headers():
    # Instantiating a Form makes sure there's a CSRF token available
    # and puts an hmac key in the session.
    form = Form()
    return {'X-CSRF-Token': form.csrf_token._value()}


class CSRFView(AdminView):
    """/csrf_token"""

    def get(self):
        return Response(headers=get_csrf_headers())
