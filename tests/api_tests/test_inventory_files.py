from helpers.request_helper import send_request

def test_get_root_certificate():
    """Verify the root certificate can be retrieved."""
    response = send_request("GET", "/mock_certs/root_ca")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pem-certificate-chain"

def test_upload_file():
    """Test uploading a file to the server."""
    files = {"file": ("test_file.txt", b"Sample file content.")}
    response = send_request("POST", "/file/add", files=files)
    assert response.status_code == 200
    assert "File uploaded successfully" in response.text
 