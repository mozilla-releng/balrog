from flask_wtf.csrf import generate_csrf


def get_csrf_headers():
    # Instantiating a Form makes sure there's a CSRF token available
    # Generate a CSRF token put an hmac key in the session.
    return {"X-CSRF-Token": generate_csrf()}
