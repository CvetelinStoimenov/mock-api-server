import unittest
import requests

class TestAPI(unittest.TestCase):

    base_url = "https://localhost:443/inventory/devices"

    def test_get_devices_success(self):
        """Test retrieving the list of devices (positive scenario)."""
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('body', data)
        self.assertTrue(len(data['body']) > 0)
        self.assertIn('id', data['body'][0])
        self.assertIn('model', data['body'][0])

    def test_get_device_by_id_success(self):
        """Test retrieving a specific device by its ID (positive scenario)."""
        device_id = "TEST1"
        response = requests.get(f"{self.base_url}/{device_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], device_id)
        self.assertIn('model', data)

    def test_get_device_not_found(self):
        """Test retrieving a non-existent device by ID (negative scenario)."""
        device_id = "NON_EXISTING_DEVICE"
        response = requests.get(f"{self.base_url}/{device_id}")
        self.assertEqual(response.status_code, 404)

    def test_add_device_success(self):
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
        response = requests.post(self.base_url, json=new_device)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['id'], new_device['id'])
        self.assertEqual(data['model'], new_device['model'])

    def test_add_device_bad_request(self):
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
        response = requests.post(self.base_url, json=new_device)
        self.assertEqual(response.status_code, 400)

    def test_update_device_success(self):
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
        response = requests.put(f"{self.base_url}/{device_id}", json=updated_device)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], updated_device['id'])
        self.assertEqual(data['ipAddress'], updated_device['ipAddress'])

    def test_update_device_not_found(self):
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
        response = requests.put(f"{self.base_url}/{device_id}", json=updated_device)
        self.assertEqual(response.status_code, 404)

    def test_delete_device_success(self):
        """Test deleting an existing device (positive scenario)."""
        device_id = "TEST1"
        response = requests.delete(f"{self.base_url}/{device_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], device_id)

    def test_delete_device_not_found(self):
        """Test deleting a non-existent device (negative scenario)."""
        device_id = "NON_EXISTENT"
        response = requests.delete(f"{self.base_url}/{device_id}")
        self.assertEqual(response.status_code, 404)

    def test_invalid_method(self):
        """Test sending a request with an unsupported HTTP method (negative scenario)."""
        response = requests.patch(self.base_url)
        self.assertEqual(response.status_code, 405)

    def test_invalid_url(self):
        """Test sending a request to an invalid URL (negative scenario)."""
        response = requests.get("http://localhost:8080/inventory/non-existent-endpoint")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()