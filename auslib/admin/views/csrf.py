from flask import jsonify
from flask_wtf import Form

from auslib.admin.views.base import AdminView

__all__ = ["CSRFView"]


def get_csrf_token():
    # Instantiating a Form makes sure there's a CSRF token available
    # and puts an hmac key in the session.
    form = Form()
    return form.csrf_token._value()


def get_csrf_headers():
    return {'X-CSRF-Token': get_csrf_token()}


class CSRFView(AdminView):
    """/csrf_token"""

    def get(self):
        token = get_csrf_token()
        data = {"csrf_token": token}
        resp = jsonify(data)
        resp.headers["X-CSRF-Token"] = token
        return resp
