import pytest


def pytest_addoption(parser):
    parser.addoption("--server_url", dest="server_url", default="https://aus4.stage.mozaws.net", help="Server to run API contract tests against")


@pytest.fixture
def server_url(request):
    return request.config.getoption("--server_url")
