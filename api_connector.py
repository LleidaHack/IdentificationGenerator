# import http.client
import requests
import json
import PrivateConfig



def send_request(endpoint: str):
    url = PrivateConfig.BASE_URL + endpoint
    headers = {
        "Authorization": "Bearer " + PrivateConfig.SERVICE_TOKEN,
    }
    r = requests.get(url, headers=headers)

# some JSON:

# parse x:
    print(json.loads(r.content)[0]['id'])
    return (json.loads(r.content))
    return r

def get_accepted():
    return send_request('/event/1/get_approved_hackers')
