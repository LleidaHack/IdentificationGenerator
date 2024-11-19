import requests
import json
import PrivateConfig


def send_request(endpoint: str, bearer: bool = True):
    url = PrivateConfig.BASE_URL + endpoint
    headers = {
        "Authorization": "Bearer " + PrivateConfig.SERVICE_TOKEN,
    }
    r = requests.get(url, headers=headers) if bearer else requests.get(url)
    return (json.loads(r.content))

def get_hackeps():
    return send_request("/v1/event/get_hackeps")["id"]

def get_accepted():
    return send_request(f'/v1/event/{get_hackeps()}/get_approved_hackers')

def get_by_tier(tier):
    return send_request(f'/v1/company/tier/{tier}/')