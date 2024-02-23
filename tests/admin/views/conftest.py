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
    from auslib.web.admin.base import connexion_app as app

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
