import pytest

from auslib.global_state import dbo


@pytest.fixture(scope="function")
def pinning_db(db_schema):
    dbo.setDb("sqlite:///:memory:")
    db_schema.create_all(dbo.engine)
    dbo.pinnable_releases.t.insert().execute(
        product="test_product",
        version="1.",
        channel="test_channel",
        mapping="test_mapping",
        data_version=1,
    )


@pytest.mark.usefixtures("pinning_db")
def test_get_pin(api):
    ret = api.get("/v2/pins/test_product/test_channel/1.")
    assert ret.status_code == 200, ret.text
    expected = {
        "product": "test_product",
        "version": "1.",
        "channel": "test_channel",
        "mapping": "test_mapping",
        "data_version": 1,
    }
    assert ret.json() == expected


@pytest.mark.usefixtures("pinning_db")
def test_get_pin_404(api):
    ret = api.get("/v2/pins/test_product/test_channel/2.")
    assert ret.status_code == 404, ret.text
