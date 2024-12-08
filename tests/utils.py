import time
import requests

def wait_for_server(url, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Server is ready at {url}")
                return True
        except requests.ConnectionError:
            print("Waiting for the server to start...")
        time.sleep(1)
    raise TimeoutError(f"Server did not become ready within {timeout} seconds.")