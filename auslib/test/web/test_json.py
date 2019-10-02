import pytest

from auslib.blobs.base import createBlob
from auslib.global_state import dbo
from auslib.web.public.base import app


@pytest.fixture(scope="function")
def disable_errorhandler(monkeypatch):
    monkeypatch.setattr(app, "error_handler_spec", {None: {}})


@pytest.fixture(scope="module")
def appconfig():
    app.config["WHITELISTED_DOMAINS"] = {"good.com": ("Guardian",)}


@pytest.fixture(scope="module")
def guardian_db(db_schema):
    db_schema.create_all(dbo.engine)
    dbo.releases.t.insert().execute(
        name="Guardian-1.0.0.0",
        product="Guardian",
        data_version=1,
        data=createBlob(
            """
{
    "name": "Guardian-1.0",
    "product": "Guardian",
    "schema_version": 10000,
    "version": "1.0.0.0",
    "required": true,
    "platforms": {
        "WINNT_x86_64": {
            "fileUrl": "https://good.com/1.0.0.0.msi"
        },
        "Darwin_x86_64": {
            "fileUrl": "https://good.com/1.0.0.0.dmg"
        }
    }
}
"""
        ),
    )
    dbo.rules.t.insert().execute(
        priority=100, backgroundRate=100, mapping="Guardian-1.0.0.0", update_type="minor", product="Guardian", channel="release", data_version=1
    )


@pytest.fixture(scope="module")
def client():
    return app.test_client()


@pytest.mark.usefixtures("appconfig", "guardian_db", "disable_errorhandler")
@pytest.mark.parametrize(
    "version,buildTarget,channel,code,response",
    [
        ("0.2.0.0", "WINNT_x86_64", "release", 200, {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0"}),
        ("0.99.99.99", "WINNT_x86_64", "release", 200, {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0"}),
        ("1.0.0.0", "WINNT_x86_64", "release", 404, {}),
        ("0.2.0.0", "Linux_x86_64", "release", 404, {}),
        ("0.2.0.0", "WINNT_x86_64", "beta", 404, {}),
    ],
)
def testGuardianResponse(client, version, buildTarget, channel, code, response):
    ret = client.get(f"/json/1/Guardian/{version}/{buildTarget}/{channel}/update.json")
    assert ret.status_code == code
    if code == 200:
        assert ret.mimetype == "application/json"
        assert ret.get_json() == response


# test that ensures unused fields are ignored
