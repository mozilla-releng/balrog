import pytest

from auslib.AUS import FORCE_FALLBACK_MAPPING, FORCE_MAIN_MAPPING
from auslib.blobs.base import createBlob
from auslib.global_state import dbo
from auslib.web.public.base import app


@pytest.fixture(scope="function")
def disable_errorhandler(monkeypatch):
    monkeypatch.setattr(app, "error_handler_spec", {None: {}})


@pytest.fixture(scope="function")
def mock_autograph(monkeypatch):
    monkeypatch.setitem(app.config, "AUTOGRAPH_URL", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_KEYID", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_USERNAME", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_PASSWORD", "fake")

    def mockreturn(*args):
        return ("abcdef", "https://this.is/a.x5u")

    import auslib.web.public.helpers

    monkeypatch.setattr(auslib.web.public.helpers, "sign_hash", mockreturn)


@pytest.fixture(scope="module")
def appconfig():
    app.config["ALLOWLISTED_DOMAINS"] = {"good.com": ("Guardian",)}


@pytest.fixture(scope="module")
def guardian_db(db_schema):
    db_schema.create_all(dbo.engine)
    dbo.releases.t.insert().execute(
        name="Guardian-Evil-1.0.0.0",
        product="Guardian",
        data_version=1,
        data=createBlob(
            """
{
    "name": "Guardian-Evil-1.0.0.0",
    "product": "Guardian",
    "schema_version": 10000,
    "version": "1.0.0.0",
    "required": true,
    "hashFunction": "sha512",
    "platforms": {
        "Darwin_x86_64": {
            "fileUrl": "https://evil.com/1.0.0.0.dmg",
            "hashValue": "ghijkl"
        }
    }
}
"""
        ),
    )
    dbo.rules.t.insert().execute(
        priority=150,
        backgroundRate=100,
        mapping="Guardian-Evil-1.0.0.0",
        update_type="minor",
        product="Guardian",
        channel="release",
        osVersion="EvilOS",
        data_version=1,
        comment="Bogus rule with osVersion set",
    )
    dbo.rules.t.insert().execute(
        priority=150,
        backgroundRate=100,
        mapping="Guardian-Evil-1.0.0.0",
        update_type="minor",
        product="Guardian",
        channel="evilrelease",
        data_version=1,
    )
    dbo.releases.t.insert().execute(
        name="Guardian-0.5.0.0",
        product="Guardian",
        data_version=1,
        data=createBlob(
            """
{
    "name": "Guardian-0.5.0.0",
    "product": "Guardian",
    "schema_version": 10000,
    "version": "0.5.0.0",
    "required": true,
    "hashFunction": "sha512",
    "platforms": {
        "WINNT_x86_64": {
            "fileUrl": "https://good.com/0.5.0.0.msi",
            "hashValue": "abcdef"
        },
        "Darwin_x86_64": {
            "fileUrl": "https://good.com/0.5.0.0.dmg",
            "hashValue": "ghijkl"
        }
    }
}
"""
        ),
    )
    dbo.releases.t.insert().execute(
        name="Guardian-1.0.0.0",
        product="Guardian",
        data_version=1,
        data=createBlob(
            """
{
    "name": "Guardian-1.0.0.0",
    "product": "Guardian",
    "schema_version": 10000,
    "version": "1.0.0.0",
    "required": true,
    "hashFunction": "sha512",
    "platforms": {
        "WINNT_x86_64": {
            "fileUrl": "https://good.com/1.0.0.0.msi",
            "hashValue": "mnopqr"
        },
        "Darwin_x86_64": {
            "fileUrl": "https://good.com/1.0.0.0.dmg",
            "hashValue": "stuvwx"
        }
    }
}
"""
        ),
    )
    dbo.rules.t.insert().execute(
        priority=120,
        backgroundRate=100,
        mapping="Guardian-0.5.0.0",
        update_type="minor",
        product="Guardian",
        channel="release",
        version="<0.5.0.0",
        data_version=1,
    )
    # fmt: off
    # to force this on multiple lines
    dbo.rules.t.insert().execute(
        priority=100,
        backgroundRate=100,
        mapping="Guardian-1.0.0.0",
        update_type="minor",
        product="Guardian",
        channel="release",
        data_version=1
    )
    dbo.rules.t.insert().execute(
        priority=100,
        backgroundRate=0,
        mapping="Guardian-1.0.0.0",
        fallbackMapping="Guardian-0.5.0.0",
        update_type="minor",
        product="Guardian",
        channel="release-rollout",
        data_version=1
    )
    # fmt: on
    dbo.rules.t.insert().execute(
        priority=100,
        backgroundRate=100,
        mapping="Guardian-1.0.0.0",
        update_type="minor",
        product="Guardian",
        channel="alpha",
        osVersion="igonred",
        buildID="12345",
        locale="ignored",
        memory="123",
        instructionSet="ignored",
        jaws=True,
        mig64=False,
        distribution="ignored",
        distVersion="ignored",
        headerArchitecture="ignored",
        data_version=1,
    )


@pytest.fixture(scope="module")
def client():
    return app.test_client()


@pytest.mark.usefixtures("appconfig", "guardian_db", "disable_errorhandler", "mock_autograph")
@pytest.mark.parametrize(
    "version,buildTarget,channel,code,response",
    [
        (
            "0.4.0.0",
            "WINNT_x86_64",
            "release",
            200,
            {"required": True, "url": "https://good.com/0.5.0.0.msi", "version": "0.5.0.0", "hashFunction": "sha512", "hashValue": "abcdef"},
        ),
        (
            "0.6.0.0",
            "WINNT_x86_64",
            "release",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
        (
            "0.99.99.99",
            "WINNT_x86_64",
            "release",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
        ("1.0.0.0", "WINNT_x86_64", "release", 404, {}),
        ("0.6.0.0", "Linux_x86_64", "release", 404, {}),
        ("0.6.0.0", "WINNT_x86_64", "beta", 404, {}),
        # This shouldn't match because the rule on the alpha channel contains fields not used by this type of update query.
        ("0.6.0.0", "WINNT_x86_64", "alpha", 404, {}),
        ("0.6.0.0", "Darwin_x86_64", "evilrelease", 200, {}),
    ],
)
def testGuardianResponse(client, version, buildTarget, channel, code, response):
    ret = client.get(f"/json/1/Guardian/{version}/{buildTarget}/{channel}/update.json")
    assert ret.status_code == code
    if code == 200:
        assert ret.mimetype == "application/json"
        assert ret.get_json() == response
        assert ret.headers["Content-Signature"] == "x5u=https://this.is/a.x5u; p384ecdsa=abcdef"
        assert "Rule-ID" in ret.headers
        assert "Rule-Data-Version" in ret.headers


@pytest.mark.usefixtures("appconfig", "guardian_db", "disable_errorhandler")
@pytest.mark.parametrize(
    "version,buildTarget,channel,code,response",
    [
        (
            "0.4.0.0",
            "WINNT_x86_64",
            "release",
            200,
            {"required": True, "url": "https://good.com/0.5.0.0.msi", "version": "0.5.0.0", "hashFunction": "sha512", "hashValue": "abcdef"},
        ),
        (
            "0.6.0.0",
            "WINNT_x86_64",
            "release",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
        (
            "0.99.99.99",
            "WINNT_x86_64",
            "release",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
    ],
)
def testGuardianResponseWithoutSigning(client, version, buildTarget, channel, code, response):
    ret = client.get(f"/json/1/Guardian/{version}/{buildTarget}/{channel}/update.json")
    assert ret.status_code == code
    if code == 200:
        assert ret.mimetype == "application/json"
        assert ret.get_json() == response
        assert "Content-Signature" not in ret.headers


@pytest.mark.usefixtures("appconfig", "guardian_db", "disable_errorhandler", "mock_autograph")
@pytest.mark.parametrize(
    "forceValue,response",
    [
        (FORCE_MAIN_MAPPING, {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"}),
        (
            FORCE_FALLBACK_MAPPING,
            {"required": True, "url": "https://good.com/0.5.0.0.msi", "version": "0.5.0.0", "hashFunction": "sha512", "hashValue": "abcdef"},
        ),
        (None, {"required": True, "url": "https://good.com/0.5.0.0.msi", "version": "0.5.0.0", "hashFunction": "sha512", "hashValue": "abcdef"}),
    ],
)
def testGuardianResponseWithGradualRollout(client, forceValue, response):
    qs = {}
    if forceValue:
        qs["force"] = forceValue.query_value
    ret = client.get("/json/1/Guardian/0.4.0.0/WINNT_x86_64/release-rollout/update.json", query_string=qs)
    assert ret.status_code == 200
    assert ret.mimetype == "application/json"
    assert ret.get_json() == response
    assert ret.headers["Content-Signature"] == "x5u=https://this.is/a.x5u; p384ecdsa=abcdef"
