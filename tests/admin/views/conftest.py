import pytest

import auslib.web.admin.views.base


@pytest.fixture(scope="function")
def mock_verified_userinfo(monkeypatch):
    def my_userinfo(*args, **kwargs):
        # TODO: Can we paramtrize this somehow?
        return {"email": "bob"}

    monkeypatch.setattr(auslib.web.admin.views.base, "verified_userinfo", my_userinfo)


@pytest.fixture(scope="session")
def api():
    from auslib.web.admin.base import app

    app.config["SECRET_KEY"] = "notasecret"
    app.config["CORS_ORIGINS"] = "*"
    app.config["AUTH_DOMAIN"] = "balrog.test.dev"
    app.config["AUTH_AUDIENCE"] = "balrog test"

    return app.test_client()
