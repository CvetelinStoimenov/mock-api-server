# Devices API Test Cases

## Test Case 1: Get all devices
- **Test Case ID**: TC_INV_001
- **Title**: Verify all devices are listed
- **Pre-conditions**: API server is running and have devices
- **Test Steps**:
  1. Send a GET request to `/inventory/devices`
  2. Verify the response status is 200 OK
  3. Verify the response body contains the expected list of devices
- **Expected Result**:
  - Status code: 200
  - Response body contains device information with fields like `id`, `ipAddress`, `model`, `serialNum`, `version`, etc.
---
## Test Case 2: Get a single device by ID
- **Test Case ID**: TC_INV_002
- **Title**: Verify searching device by ID is listed
- **Pre-conditions**: API server is running, and a device with `id` TEST1 exists
- **Test Steps**:
  1. Send a GET request to `/inventory/devices/TEST1`
  2. Verify the response status is 200 OK
  3. Verify the response body contains the correct device details for `TEST1`
- **Expected Result**:
  - Status code: 200
  - Response body matches the details of the device with `id` TEST1
---
## Test Case 3: Attempt to get a device that does not exist
- **Test Case ID**: TC_INV_003
- **Title**: Verify error handling when a non-existent device is searching
- **Pre-conditions**: API server is running
- **Test Steps**:
  1. Send a GET request to `/inventory/devices/NON_EXISTING_DEVICE`
  2. Verify the response status is 404 Not Found
- **Expected Result**:
  - Status code: 404
  - Response body contains an error message indicating the device does not exist
---
## Test Case 4: Add a new device (valid input)
- **Test Case ID**: TC_INV_004
- **Title**: Verify adding a new device to the inventory
- **Pre-conditions**: API server is running
- **Test Steps**:
  1. Send a POST request to `/inventory/devices` with the following body:
    ```json
    {
      "id": "TEST3",
      "ipAddress": "10.0.49.142",
      "deviceAddresses": {
        "fqdn": "test3.com",
        "ipv4Address": "10.0.49.142",
        "ipv6Address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
      },
      "model": "TEST_DEVICE",
      "serialNum": "TEST3-1xyz1234",
      "version": "4.0.0",
      "build": "20240410.2024-8f4e21xyz"
    }
    ```
  2. Verify the response status is 201 Created
  3. Verify the response body contains the added device data with the same `id`, `ipAddress`, etc.
- **Expected Result**:
  - Status code: 201
  - Response body contains the new device details
---
## Test Case 5: Add a new device (missing required field)
- **Test Case ID**: TC_INV_005
- **Title**: Verify handling missing required fields when adding a device
- **Pre-conditions**: API server is running
- **Test Steps**:
  1. Send a POST request to `/inventory/devices` with the following body (missing `model`):
    ```json
    {
      "id": "TEST4",
      "ipAddress": "10.0.49.143",
      "deviceAddresses": {
        "fqdn": "test4.com",
        "ipv4Address": "10.0.49.143",
        "ipv6Address": "2001:0db8:85a3:0000:0000:8a2e:0370:7335"
      },
      "serialNum": "TEST4-1abc5678",
      "version": "4.1.0",
      "build": "20240410.2025-8f4e21abc"
    }
    ```
  2. Verify the response status is 400 Bad Request
  3. Verify the response body contains an error message indicating the missing `model` field
- **Expected Result**:
  - Status code: 400
  - Response body contains an error message about the missing field
---
## Test Case 6: Update an existing device (valid input)
- **Test Case ID**: TC_INV_006
- **Title**: Verify updating an existing device
- **Pre-conditions**: API server is running, and a device with `id` TEST1 exists
- **Test Steps**:
  1. Send a PUT request to `/inventory/devices/TEST1` with the following body:
    ```json
    {
      "id": "TEST1",
      "ipAddress": "10.0.49.140",
      "deviceAddresses": {
        "fqdn": "test1.com",
        "ipv4Address": "10.0.49.140",
        "ipv6Address": null
      },
      "model": "TEST_DEVICE_UPDATED",
      "serialNum": "TEST1-1updated1234",
      "version": "3.0.0",
      "build": "20240410.2026-8f4e21updated"
    }
    ```
  2. Verify the response status is 200 OK
  3. Verify the response body contains the updated device details
- **Expected Result**:
  - Status code: 200
  - Response body contains updated details for `TEST1`
---
## Test Case 7: Attempt to update a non-existent device
- **Test Case ID**: TC_INV_007
- **Title**: Verify error handling when updating a non-existent device
- **Pre-conditions**: API server is running
- **Test Steps**:
  1. Send a PUT request to `/inventory/devices/UNKNOWN_ID` with any valid body
  2. Verify the response status is 404 Not Found
- **Expected Result**:
  - Status code: 404
  - Response body contains an error message indicating the device does not exist
---
## Test Case 8: Delete a device by ID
- **Test Case ID**: TC_INV_008
- **Title**: Verify deleting a device by ID
- **Pre-conditions**: API server is running, and a device with `id` TEST2 exists
- **Test Steps**:
  1. Send a DELETE request to `/inventory/devices/TEST2`
  2. Verify the response status is 200 OK
  3. Verify the device is no longer retrievable using GET `/inventory/devices/TEST2`
- **Expected Result**:
  - Status code: 200
  - Device with `id` TEST2 no longer exists in the system
---
## Test Case 9: Attempt to delete a non-existent device
- **Test Case ID**: TC_INV_009
- **Title**: Verify error handling when deleting a non-existent device
- **Pre-conditions**: API server is running
- **Test Steps**:
  1. Send a DELETE request to `/inventory/devices/UNKNOWN_ID`
  2. Verify the response status is 404 Not Found
- **Expected Result**:
  - Status code: 404
  - Response body contains an error message indicating the device does not exist
---
## Test Case 10: Attempt to use an unsupported HTTP method
- **Test Case ID**: TC_INV_010
- **Title**: Verify error handling for unsupported HTTP methods
- **Pre-conditions**: API server is running
- **Test Steps**:
  1. Send a PATCH request to `/inventory/devices`
  2. Verify the response status is 405 Method Not Allowed
- **Expected Result**:
  - Status code: 405
  - Response body contains an error message indicating the method is not supported

---

## Test Case 11: Access a non-existent endpoint
- **Test Case ID**: TC_INV_011
- **Title**: Verify response for a non-existent endpoint
- **Pre-conditions**: API server is running
- **Test Steps**:
  1. Send a GET request to `/inventory/non-existent-endpoint`
  2. Verify the response status is 404 Not Found
- **Expected Result**:
  - Status code: 404
  - Response body contains an error message indicating the resource is not found
