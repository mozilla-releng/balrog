from unittest.mock import MagicMock

import pytest
from mock import mock

import auslib.web.public.helpers
import auslib.web.public.json
from auslib.AUS import FORCE_FALLBACK_MAPPING, FORCE_MAIN_MAPPING
from auslib.blobs.base import createBlob
from auslib.global_state import dbo
from auslib.web.public.base import create_app


@pytest.fixture(scope="module")
def app():
    connexion_app = create_app()
    app = connexion_app.app
    app.testing = True
    return connexion_app.app


@pytest.fixture(scope="function")
def mock_autograph(monkeypatch, app):
    monkeypatch.setitem(app.config, "AUTOGRAPH_URL", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_KEYID", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_USERNAME", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_PASSWORD", "fake")

    def mockreturn(*args):
        return ("abcdef", "https://this.is/a.x5u")

    monkeypatch.setattr(auslib.web.public.helpers, "sign_hash", mockreturn)
    monkeypatch.setattr(auslib.web.public.helpers, "make_hash", MagicMock())


@pytest.fixture(scope="module")
def appconfig(app):
    app.config["ALLOWLISTED_DOMAINS"] = {"good.com": ("Guardian",)}


@pytest.fixture(scope="module")
def guardian_db():
    dbo.setDb("sqlite:///:memory:")
    dbo.create()
    dbo.metadata.create_all(dbo.engine)
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
        name="Guardian-0.6.0.0",
        product="Guardian",
        data_version=1,
        data=createBlob(
            """
{
    "name": "Guardian-0.6.0.0",
    "product": "Guardian",
    "schema_version": 10000,
    "version": "0.6.0.0",
    "required": true,
    "hashFunction": "sha512",
    "platforms": {
        "WINNT_x86_64": {
            "fileUrl": "https://good.com/0.6.0.0.msi",
            "hashValue": "abcpqr"
        },
        "Darwin_x86_64": {
            "fileUrl": "https://good.com/0.6.0.0.dmg",
            "hashValue": "ghivwx"
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
    dbo.rules.t.insert().execute(
        priority=110,
        backgroundRate=100,
        mapping="Guardian-0.6.0.0",
        update_type="minor",
        product="Guardian",
        osVersion="obsolete",
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
        osVersion="ignored",
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
    dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="b", update_type="minor", product="b", data_version=1, alias="moz-releng")
    dbo.rules.t.insert().execute(priority=91, backgroundRate=100, mapping="b", update_type="minor", product="b", data_version=1, locale="loc", alias="locale")
    dbo.releases.t.insert().execute(
        name="b",
        product="b",
        data_version=1,
        data=createBlob(
            """
{
    "name": "b",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "2",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/z"
                    }
                },
                "xh": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "6",
                        "fileUrl": "http://a.com/x"
                    }
                }
            }
        }
    }
}
"""
        ),
    )


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.mark.usefixtures("appconfig", "guardian_db", "mock_autograph")
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
def testGuardianResponseV1(client, version, buildTarget, channel, code, response):
    with mock.patch("auslib.web.public.base.statsd.pipeline") as mocked_pipeline:
        ret = client.get(f"/json/1/Guardian/{version}/{buildTarget}/{channel}/update.json")
        assert ret.status_code == code
        assert mocked_pipeline.mock_calls.count(mock.call().incr(f"response.json.{code}")) == 1
        if code == 200:
            assert ret.mimetype == "application/json"
            assert ret.get_json() == response
            assert ret.headers["Content-Signature"] == "x5u=https://this.is/a.x5u; p384ecdsa=abcdef"
            auslib.web.public.helpers.make_hash.assert_called_once_with(ret.text)
            assert "Rule-ID" in ret.headers
            assert "Rule-Data-Version" in ret.headers


@pytest.mark.usefixtures("appconfig", "guardian_db")
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
def testGuardianResponseV1WithoutSigning(client, version, buildTarget, channel, code, response):
    ret = client.get(f"/json/1/Guardian/{version}/{buildTarget}/{channel}/update.json")
    assert ret.status_code == code
    if code == 200:
        assert ret.mimetype == "application/json"
        assert ret.get_json() == response
        assert "Content-Signature" not in ret.headers


@pytest.mark.usefixtures("appconfig", "guardian_db", "mock_autograph")
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
def testGuardianResponseV1WithGradualRollout(client, forceValue, response):
    qs = {}
    if forceValue:
        qs["force"] = forceValue.query_value
    ret = client.get("/json/1/Guardian/0.4.0.0/WINNT_x86_64/release-rollout/update.json", query_string=qs)
    assert ret.status_code == 200
    assert ret.mimetype == "application/json"
    assert ret.get_json() == response
    assert ret.headers["Content-Signature"] == "x5u=https://this.is/a.x5u; p384ecdsa=abcdef"
    auslib.web.public.helpers.make_hash.assert_called_once_with(ret.text)


@pytest.mark.usefixtures("appconfig", "guardian_db", "mock_autograph")
@pytest.mark.parametrize(
    "version,buildTarget,channel,osVersion,code,response",
    [
        (
            "0.4.0.0",
            "WINNT_x86_64",
            "release",
            "Windows 10",
            200,
            {"required": True, "url": "https://good.com/0.5.0.0.msi", "version": "0.5.0.0", "hashFunction": "sha512", "hashValue": "abcdef"},
        ),
        (
            "0.5.0.0",
            "WINNT_x86_64",
            "release",
            "current",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
        (
            "0.5.0.0",
            "WINNT_x86_64",
            "release",
            "obsolete",
            200,
            {"required": True, "url": "https://good.com/0.6.0.0.msi", "version": "0.6.0.0", "hashFunction": "sha512", "hashValue": "abcpqr"},
        ),
        (
            "0.6.0.0",
            "WINNT_x86_64",
            "release",
            "Windows 10",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
        (
            "0.99.99.99",
            "WINNT_x86_64",
            "release",
            "Windows 10",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
        ("1.0.0.0", "WINNT_x86_64", "release", "Windows 10", 404, {}),
        ("0.6.0.0", "Linux_x86_64", "release", "Linux", 404, {}),
        ("0.6.0.0", "WINNT_x86_64", "beta", "Windows 10", 404, {}),
        # This shouldn't match because the rule on the alpha channel contains fields not used by this type of update query.
        ("0.6.0.0", "WINNT_x86_64", "alpha", "Windows 10", 404, {}),
        ("0.6.0.0", "Darwin_x86_64", "evilrelease", "Darwin 13", 200, {}),
    ],
)
def testGuardianResponseV2(client, version, buildTarget, channel, osVersion, code, response):
    ret = client.get(f"/json/2/Guardian/{version}/{buildTarget}/{channel}/{osVersion}/update.json")
    assert ret.status_code == code
    if code == 200:
        assert ret.mimetype == "application/json"
        assert ret.get_json() == response
        assert ret.headers["Content-Signature"] == "x5u=https://this.is/a.x5u; p384ecdsa=abcdef"
        auslib.web.public.helpers.make_hash.assert_called_once_with(ret.text)
        assert "Rule-ID" in ret.headers
        assert "Rule-Data-Version" in ret.headers


@pytest.mark.usefixtures("appconfig", "guardian_db")
@pytest.mark.parametrize(
    "version,buildTarget,channel,osVersion,code,response",
    [
        (
            "0.4.0.0",
            "WINNT_x86_64",
            "release",
            "Windows 10",
            200,
            {"required": True, "url": "https://good.com/0.5.0.0.msi", "version": "0.5.0.0", "hashFunction": "sha512", "hashValue": "abcdef"},
        ),
        (
            "0.6.0.0",
            "WINNT_x86_64",
            "release",
            "Windows 10",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
        (
            "0.99.99.99",
            "WINNT_x86_64",
            "release",
            "Windows 10",
            200,
            {"required": True, "url": "https://good.com/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "mnopqr"},
        ),
    ],
)
def testGuardianResponseV2WithoutSigning(client, version, buildTarget, channel, osVersion, code, response):
    ret = client.get(f"/json/2/Guardian/{version}/{buildTarget}/{channel}/{osVersion}/update.json")
    assert ret.status_code == code
    if code == 200:
        assert ret.mimetype == "application/json"
        assert ret.get_json() == response
        assert "Content-Signature" not in ret.headers


@pytest.mark.usefixtures("appconfig", "guardian_db", "mock_autograph")
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
def testGuardianResponseV2WithGradualRollout(client, forceValue, response):
    qs = {}
    if forceValue:
        qs["force"] = forceValue.query_value
    ret = client.get("/json/2/Guardian/0.4.0.0/WINNT_x86_64/release-rollout/Windows%2010/update.json", query_string=qs)
    assert ret.status_code == 200
    assert ret.mimetype == "application/json"
    assert ret.get_json() == response
    assert ret.headers["Content-Signature"] == "x5u=https://this.is/a.x5u; p384ecdsa=abcdef"
    auslib.web.public.helpers.make_hash.assert_called_once_with(ret.text)


@pytest.mark.usefixtures("guardian_db")
def testXMLForGuardianBlob(client):
    ret = client.get("/update/1/Guardian/0.4.0.0/default/WINNT_x86_64/en-US/release/update.xml")
    assert ret.status_code == 400


@pytest.mark.usefixtures("guardian_db")
def testJSONForAppReleaseBlob(client):
    ret = client.get("/json/1/b/127.0/p/release/update.json")
    assert ret.status_code < 500
    ret = client.get("/json/2/b/127.0/p/release/default/update.json")
    assert ret.status_code < 500
