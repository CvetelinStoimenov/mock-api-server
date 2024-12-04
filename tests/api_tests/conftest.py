import pytest
from helpers.cert_helper import fetch_certificate

@pytest.fixture(scope="session", autouse=True)
def setup_certificates():
    """Ensure root CA certificate is available before running tests."""
    cert_path = fetch_certificate()
    return cert_path
