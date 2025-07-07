from collections import defaultdict

import pytest

from auslib.web.public.base import create_app


@pytest.fixture(scope="class")
def app(request):
    connexion_app = create_app()
    app = request.cls.app = connexion_app.app
    return app


@pytest.fixture(scope="class")
def propagate_exceptions(app):
    # Error handlers are removed in order to give us better debug messages
    # Ripped from https://github.com/pallets/flask/blob/2.3.3/src/flask/scaffold.py#L131-L134
    app.error_handler_spec = defaultdict(lambda: defaultdict(dict))
