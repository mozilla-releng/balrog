from unittest.mock import MagicMock

import auslib.web.public.helpers
from auslib.blobs.base import createBlob
from auslib.global_state import cache, dbo


def test_get_content_signature_headers(monkeypatch):
    mockapp = MagicMock()
    mockapp.config = {
        "AUTOGRAPH_product_URL": "foo://bar",
        "AUTOGRAPH_product_KEYID": "fookeyid",
        "AUTOGRAPH_product_USERNAME": "foousername",
        "AUTOGRAPH_product_PASSWORD": "foopassword",
    }
    monkeypatch.setattr("auslib.web.public.helpers.app", mockapp)

    content = "some content"
    product = "product"

    x5u = "https://this.is/a.x5u"
    ecdsa = "foobar"

    def mock_sign_hash(_, key, *__):
        if key == "fookeyid":
            return (ecdsa, x5u)
        raise ValueError(f"Unexpected key {key}")

    mocksign = MagicMock()
    mocksign.side_effect = mock_sign_hash
    monkeypatch.setattr(auslib.web.public.helpers, "sign_hash", mocksign)

    assert auslib.web.public.helpers.get_content_signature_headers(content, product) == {"Content-Signature": f"x5u={x5u}; p384ecdsa={ecdsa}"}

    assert mocksign.call_count == 1


def test_warm_caches(db_schema, insert_release, firefox_54_0_1_build1, firefox_67_0_build1, superblob_e8f4a19, hotfix_bug_1548973_1_1_4, timecop_1_0):
    dbo.setDb("sqlite:///:memory:")
    db_schema.create_all(dbo.engine)
    dbo.rules.t.insert().execute(
        rule_id=5,
        priority=90,
        backgroundRate=100,
        mapping="Firefox-67.0-build1",
        fallbackMapping="Firefox-54.0.1-build1",
        update_type="minor",
        product="Firefox",
        mig64=True,
        data_version=1,
    )
    dbo.rules.t.insert().execute(
        priority=300,
        product="SystemAddons",
        channel="releasesjson",
        mapping="Superblob-e8f4a19cfd695bf0eb66a2115313c31cc23a2369c0dc7b736d2f66d9075d7c66",
        backgroundRate=100,
        update_type="minor",
        data_version=1,
    )
    dbo.releases.t.insert().execute(
        name="Firefox-54.0.1-build1",
        product="Firefox",
        data_version=1,
        data=createBlob(firefox_54_0_1_build1),
    )
    insert_release(firefox_67_0_build1, "Firefox", history=False)
    insert_release(superblob_e8f4a19, "SystemAddons", history=False)
    insert_release(hotfix_bug_1548973_1_1_4, "SystemAddons", history=False)
    insert_release(timecop_1_0, "SystemAddons", history=False)
    cache.reset()
    cache.make_cache("blob", 50, 3600)
    cache.make_cache("releases", 50, 3600)
    cache.make_cache("release_assets", 50, 3600)

    for cache_name in ("blob", "releases", "release_assets"):
        c = cache.caches[cache_name]
        assert c.lookups == 0, cache_name
        assert c.hits == 0, cache_name
        assert c.misses == 0, cache_name

    auslib.web.public.helpers.warm_caches()

    # one lookup per release, all misses
    assert cache.caches["blob"].lookups == 1
    assert cache.caches["blob"].hits == 0
    assert cache.caches["blob"].misses == 1
    for cache_name in ("releases", "release_assets"):
        c = cache.caches[cache_name]
        # There are 13 lookups here, which cover the following:
        # - an attempt to look up 54.0.1 in this table                (1)
        # - an attempt to look up the 3 releases referenced by 54.0.1 (4)
        # - the superblob                                             (5)
        # - the two releases referenced by the superblob              (7)
        # - 67.0                                                      (8)
        # - the 5 releases referenced by 67.0                         (13)
        assert c.lookups == 13, cache_name
        assert c.hits == 0, cache_name
        assert c.misses == 13, cache_name

    auslib.web.public.helpers.warm_caches()

    # another lookup per release, all hits this time
    assert cache.caches["blob"].lookups == 2
    assert cache.caches["blob"].hits == 1
    assert cache.caches["blob"].misses == 1
    for cache_name in ("releases", "release_assets"):
        c = cache.caches[cache_name]
        assert c.lookups == 26, cache_name
        assert c.hits == 13, cache_name
        assert c.misses == 13, cache_name
