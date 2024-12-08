import os
import json
import requests

def fetch_certificate():
    """Download root CA certificate for HTTPS verification."""
    with open("tests/config/config.json", "r") as config_file:
        config = json.load(config_file)

    # Use https or http base URL based on the config
    base_url = config['base_url_https'] if config['use_https'] else config['base_url_http']
    
    cert_path = config["cert_path"]
    os.makedirs(os.path.dirname(cert_path), exist_ok=True)

    response = requests.get(f"{base_url}/mock_certs/root_ca", verify=False)
    if response.status_code == 200:
        with open(cert_path, "wb") as cert_file:
            cert_file.write(response.content)
    else:
        raise RuntimeError("Failed to fetch root CA certificate")

    return cert_path
