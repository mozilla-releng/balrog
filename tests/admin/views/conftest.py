import pytest

import auslib.web.admin.base


@pytest.fixture(scope="function")
def mock_verified_userinfo(monkeypatch):
    def mock_userinfo(username="bob"):
        def my_userinfo(*args, **kwargs):
            return {"email": username}

        monkeypatch.setattr(auslib.web.admin.base, "verified_userinfo", my_userinfo)

    mock_userinfo()
    return mock_userinfo


@pytest.fixture(scope="session")
def api():
    from auslib.web.admin.base import connexion_app, flask_app

    flask_app.config["SECRET_KEY"] = "notasecret"
    flask_app.config["CORS_ORIGINS"] = "*"
    flask_app.config["AUTH_DOMAIN"] = "balrog.test.dev"
    flask_app.config["AUTH_AUDIENCE"] = "balrog test"
    flask_app.config["M2M_ACCOUNT_MAPPING"] = {}
    flask_app.config["ALLOWLISTED_DOMAINS"] = {
        "download.mozilla.org": ("Firefox",),
        "archive.mozilla.org": ("Firefox",),
        "cdmdownload.adobe.com": ("CDM",),
    }

    return connexion_app.test_client()
