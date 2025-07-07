import pytest

from auslib.web.public.base import create_app


@pytest.fixture(scope="class")
def app(request):
    connexion_app = create_app()
    app = request.cls.app = connexion_app.app
    app.testing = True
    return app
