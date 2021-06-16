import pytest

from auslib.util.comparison import version_compare


@pytest.mark.parametrize(
    "version, glob, expected",
    (
        ("80.0.0", "80.0.*", True),
        ("80.0.1", "80.0.*", True),
        ("800.0.1", "80.0.*", False),
        ("80.1.90", "80.1.*", True),
        ("80.10.0", "80.1.*", False),
        ("80.1.0", "80.*", True),
        ("80.9.89", "80.*", True),
        ("80.0a1", "80.*", True),
        ("89.89.0", "80.*", False),
    ),
)
def test_glob_version(version, glob, expected):
    assert version_compare(version, glob) is expected
