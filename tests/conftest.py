import pytest
from tests.utils import wait_for_server
from tests.helpers.cert_helper import fetch_certificate

@pytest.fixture(scope="session", autouse=True)
def wait_for_mock_server():
    wait_for_server("http://localhost:8080")
