import pytest

from auslib.blobs.guardian import GuardianBlob


@pytest.fixture
def guardblob():
    blob = GuardianBlob()
    blob.loadJSON(
        """
{
    "name": "Guardian-1.0.0.0",
    "product": "Guardian",
    "schema_version": 10000,
    "version": "1.0.0.0",
    "required": true,
    "platforms": {
        "WINNT_x86_64": {
            "fileUrl": "https://a.com/this/is/1.0.0.0.msi"
        },
        "Darwin_x86_64": {
            "fileUrl": "https://a.com/this/is/1.0.0.0.dmg"
        }
    }
}
"""
    )
    return blob


@pytest.mark.usefixtures("guardblob")
@pytest.mark.parametrize("whitelistedDomains,expected", [({"a.com": ("Guardian",)}, False), ({}, True)])
def testContainsForbiddenDomain(guardblob, whitelistedDomains, expected):
    assert guardblob.containsForbiddenDomain("Guardian", whitelistedDomains) is expected


@pytest.mark.usefixtures("guardblob")
@pytest.mark.parametrize(
    "version,expected", [("0.5.0.0", True), ("0.8.0.0", True), ("0.99.99.99", True), ("1.0.0.0", False), ("1.0.5.0", False), ("2.0.0.0", False)]
)
def testShouldServeUpdateVariousVersions(guardblob, version, expected):
    updateQuery = {"product": "Guardian", "version": version, "buildTarget": "WINNT_x86_64", "channel": "release"}
    assert guardblob.shouldServeUpdate(updateQuery) is expected


@pytest.mark.usefixtures("guardblob")
def testShouldServeUpdateMissingBuildTarget(guardblob):
    updateQuery = {"product": "Guardian", "version": "0.5.0.0", "buildTarget": "Linux_x86_64", "channel": "release"}
    assert not guardblob.shouldServeUpdate(updateQuery)


@pytest.mark.usefixtures("guardblob")
@pytest.mark.parametrize(
    "buildTarget,whitelistedDomains,expected",
    [
        ("WINNT_x86_64", {"a.com": ("Guardian",)}, {"required": True, "url": "https://a.com/this/is/1.0.0.0.msi", "version": "1.0.0.0"}),
        ("Darwin_x86_64", {"a.com": ("Guardian",)}, {"required": True, "url": "https://a.com/this/is/1.0.0.0.dmg", "version": "1.0.0.0"}),
        ("Linux_x86_64", {"a.com": ("Guardian",)}, {}),
        ("WINNT_x86_64", {}, {}),
    ],
)
def testGetResponse(guardblob, buildTarget, whitelistedDomains, expected):
    updateQuery = {"product": "Guardian", "version": "0.5.0.0", "buildTarget": buildTarget, "channel": "release"}
    assert guardblob.getResponse(updateQuery, whitelistedDomains) == expected
