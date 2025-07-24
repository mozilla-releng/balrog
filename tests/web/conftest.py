import pytest

from auslib.web.public.base import create_app


@pytest.fixture(scope="class")
def app(request):
    app = create_app()
    request.cls.app = app
    app.app.testing = True
    return app
