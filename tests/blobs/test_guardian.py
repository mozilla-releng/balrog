import pytest

from auslib.blobs.base import ServeUpdate
from auslib.blobs.guardian import GuardianBlob


@pytest.fixture(scope="session")
def guardianblob():
    blob = GuardianBlob()
    blob.loadJSON(
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
            "fileUrl": "https://a.com/this/is/1.0.0.0.msi",
            "hashValue": "abcdef"
        },
        "Darwin_x86_64": {
            "fileUrl": "https://a.com/this/is/1.0.0.0.dmg",
            "hashValue": "ghijkl"
        }
    }
}
"""
    )
    return blob


@pytest.mark.parametrize("allowlistedDomains,expected", [({"a.com": ("Guardian",)}, False), ({}, True)])
def testContainsForbiddenDomain(guardianblob, allowlistedDomains, expected):
    assert guardianblob.containsForbiddenDomain("Guardian", allowlistedDomains) is expected


@pytest.mark.parametrize(
    "version,expected",
    [
        ("0.5.0.0", ServeUpdate.Yes),
        ("0.8.0.0", ServeUpdate.Yes),
        ("0.99.99.99", ServeUpdate.Yes),
        ("1.0.0.0", ServeUpdate.No),
        ("1.0.5.0", ServeUpdate.No),
        ("2.0.0.0", ServeUpdate.No),
    ],
)
def testShouldServeUpdateVariousVersions(guardianblob, version, expected):
    updateQuery = {"product": "Guardian", "version": version, "buildTarget": "WINNT_x86_64", "channel": "release"}
    assert guardianblob.shouldServeUpdate(updateQuery) is expected


def testShouldServeUpdateMissingBuildTarget(guardianblob):
    updateQuery = {"product": "Guardian", "version": "0.5.0.0", "buildTarget": "Linux_x86_64", "channel": "release"}
    assert not guardianblob.shouldServeUpdate(updateQuery)


@pytest.mark.parametrize(
    "buildTarget,allowlistedDomains,expected",
    [
        (
            "WINNT_x86_64",
            {"a.com": ("Guardian",)},
            {"required": True, "url": "https://a.com/this/is/1.0.0.0.msi", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "abcdef"},
        ),
        (
            "Darwin_x86_64",
            {"a.com": ("Guardian",)},
            {"required": True, "url": "https://a.com/this/is/1.0.0.0.dmg", "version": "1.0.0.0", "hashFunction": "sha512", "hashValue": "ghijkl"},
        ),
        ("Linux_x86_64", {"a.com": ("Guardian",)}, {}),
        ("WINNT_x86_64", {}, {}),
    ],
)
def testGetResponse(guardianblob, buildTarget, allowlistedDomains, expected):
    updateQuery = {"product": "Guardian", "version": "0.5.0.0", "buildTarget": buildTarget, "channel": "release"}
    assert guardianblob.getResponse(updateQuery, allowlistedDomains) == expected
