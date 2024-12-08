import pytest
import sys
print("PYTHONPATH:", sys.path)
from tests.utils import wait_for_server
from helpers.cert_helper import fetch_certificate

@pytest.fixture(scope="session", autouse=True)
def wait_for_mock_server():
    wait_for_server("http://localhost:8080")