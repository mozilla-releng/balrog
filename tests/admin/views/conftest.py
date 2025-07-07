import pytest

import auslib.web.admin.base
from auslib.util.auth import AuthError
from auslib.web.admin.base import create_app


@pytest.fixture(scope="function")
def mock_verified_userinfo(monkeypatch):
    def mock_userinfo(username="bob"):
        def my_userinfo(*args, **kwargs):
            if not username:
                raise AuthError("auth required", 401)
            return {"email": username}

        monkeypatch.setattr(auslib.web.admin.base, "verified_userinfo", my_userinfo)

    mock_userinfo()
    return mock_userinfo


@pytest.fixture(scope="session")
def api():

    connexion_app = create_app()
    app = connexion_app.app
    app.testing = True
    app.config["SECRET_KEY"] = "notasecret"
    app.config["CORS_ORIGINS"] = "*"
    app.config["AUTH_DOMAIN"] = "balrog.test.dev"
    app.config["AUTH_AUDIENCE"] = "balrog test"
    app.config["M2M_ACCOUNT_MAPPING"] = {}
    app.config["ALLOWLISTED_DOMAINS"] = {
        "download.mozilla.org": ("Firefox",),
        "archive.mozilla.org": ("Firefox",),
        "cdmdownload.adobe.com": ("CDM",),
    }

    return app.test_client()


@pytest.fixture(scope="class")
def app():
    connexion_app = create_app()
    app = connexion_app.app
    app.testing = True
    return app
