from helpers.request_helper import send_request

def test_get_devices_success():
    """Verify all devices are listed successfully."""
    response = send_request("GET", "/inventory/devices")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert all("id" in device for device in data)

def test_get_devices_not_found():
    """Verify behavior when accessing an invalid endpoint."""
    response = send_request("GET", "/inventory/nonexistent")
    assert response.status_code == 404


'''
import requests
import pytest

BASE_HTTP_URL = "http://localhost:8080/inventory/devices"
BASE_HTTPS_URL = "https://localhost:443/inventory/devices"

def test_get_devices_success():
    """Test retrieving the list of devices (positive scenario)."""
    response = requests.get(BASE_HTTP_URL)
    assert response.status_code == 200
    data = response.json()

    # Check if the response is a list and contains at least one device
    assert isinstance(data, list)
    assert len(data) > 0  # Ensure there's at least one device in the list
    assert 'id' in data[0]  # Ensure the first device has an 'id' key
    assert 'model' in data[0]  # Ensure the first device has a 'model' key

def test_get_all_devices():
    """Verify all devices are listed."""
    
    # Step 1: Send a GET request to /inventory/devices
    response = requests.get(BASE_HTTP_URL)
    
    # Step 2: Verify the response status is 200 OK
    assert response.status_code == 200, f"Expected 200 OK, but got {response.status_code}"
    
    # Step 3: Verify the response body contains the expected list of devices
    data = response.json()
    
    # Check if the response is a list
    assert isinstance(data, list), f"Expected a list of devices, but got {type(data)}"
    
    # Ensure the list contains at least one device
    assert len(data) > 0, "Expected at least one device in the response body"
    
    # Check that the first device contains expected fields
    required_fields = ['id', 'ipAddress', 'model', 'serialNum', 'version']
    for field in required_fields:
        assert field in data[0], f"Missing expected field '{field}' in the first device"

def test_get_device_by_id_success():
    """Test retrieving a specific device by its ID (positive scenario)."""
    device_id = "TEST1"
    response = requests.get(f"{BASE_URL}/{device_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == device_id
    assert 'model' in data

def test_get_device_not_found():
    """Test retrieving a non-existent device by ID (negative scenario)."""
    device_id = "NON_EXISTING_DEVICE"
    response = requests.get(f"{BASE_URL}/{device_id}")
    assert response.status_code == 404

def test_add_device_success():
    """Test adding a new device to the inventory (positive scenario)."""
    new_device = {
        "id": "TEST3",
        "ipAddress": "10.0.49.142",
        "deviceAddresses": {
            "fqdn": "newdevice.com",
            "ipv4Address": "10.0.49.142",
            "ipv6Address": None
        },
        "model": "NEW_DEVICE",
        "serialNum": "TEST3-1ghfaf6a-1234-56d1-7890-abcd1234xyz",
        "version": "1.0.0",
        "build": "20240501.1200-xyz123"
    }
    response = requests.post(BASE_URL, json=new_device)
    assert response.status_code == 201
    data = response.json()
    assert data['id'] == new_device['id']
    assert data['model'] == new_device['model']

def test_add_device_bad_request():
    """Test adding a new device with missing or invalid data (negative scenario)."""
    new_device = {
        "id": "TEST4",
        "ipAddress": "10.0.49.143",
        "deviceAddresses": {
            "fqdn": "invalid.com"
        },  # Missing ipv4Address
        "model": "NEW_DEVICE_INVALID",
        "serialNum": "TEST4-1ghfaf6a-1234-56d1-7890-abcd1234xyz"
    }
    response = requests.post(BASE_URL, json=new_device)
    assert response.status_code == 400

def test_update_device_success():
    """Test updating an existing device's information (positive scenario)."""
    device_id = "TEST1"
    updated_device = {
        "id": device_id,
        "ipAddress": "10.0.49.150",
        "deviceAddresses": {
            "fqdn": "updateddevice.com",
            "ipv4Address": "10.0.49.150",
            "ipv6Address": None
        },
        "model": "UPDATED_DEVICE",
        "serialNum": "TEST1-1updated1234-41b1-86d8-acf36064f9ec",
        "version": "2.4.0",
        "build": "20240411.1854-updated"
    }
    response = requests.put(f"{BASE_URL}/{device_id}", json=updated_device)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == updated_device['id']
    assert data['ipAddress'] == updated_device['ipAddress']

def test_update_device_not_found():
    """Test updating a non-existent device (negative scenario)."""
    device_id = "NON_EXISTENT"
    updated_device = {
        "id": device_id,
        "ipAddress": "10.0.49.150",
        "deviceAddresses": {
            "fqdn": "updateddevice.com",
            "ipv4Address": "10.0.49.150",
            "ipv6Address": None
        },
        "model": "UPDATED_DEVICE",
        "serialNum": "TEST_NON_EXISTENT-1234-5678-9101-11223344",
        "version": "2.4.0",
        "build": "20240411.1854-updated"
    }
    response = requests.put(f"{BASE_URL}/{device_id}", json=updated_device)
    assert response.status_code == 404

def test_delete_device_success():
    """Test deleting an existing device (positive scenario)."""
    device_id = "TEST1"
    response = requests.delete(f"{BASE_URL}/{device_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == device_id

def test_delete_device_not_found():
    """Test deleting a non-existent device (negative scenario)."""
    device_id = "NON_EXISTENT"
    response = requests.delete(f"{BASE_URL}/{device_id}")
    assert response.status_code == 404

def test_invalid_method():
    """Test sending a request with an unsupported HTTP method (negative scenario)."""
    response = requests.patch(BASE_URL)
    assert response.status_code == 405

def test_invalid_url():
    """Test sending a request to an invalid URL (negative scenario)."""
    response = requests.get("http://localhost:8080/inventory/non-existent-endpoint")
    assert response.status_code == 404'''