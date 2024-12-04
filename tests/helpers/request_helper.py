import requests
import json

def get_base_url():
    with open("config/config.json", "r") as config_file:
        config = json.load(config_file)

    if config["use_https"]:
        return config["base_url_https"], config["cert_path"]
    else:
        return config["base_url_http"], None

def send_request(method, endpoint, **kwargs):
    base_url, cert_path = get_base_url()
    url = f"{base_url}{endpoint}"

    if cert_path:
        return requests.request(method, url, verify=cert_path, **kwargs)
    else:
        return requests.request(method, url, verify=False, **kwargs)
