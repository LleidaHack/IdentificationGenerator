import requests
import json
import os
from config.settings import settings

BASE_URL = settings.BASE_URL
SERVICE_TOKEN = settings.SERVICE_TOKEN

class APIService:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = SERVICE_TOKEN

    def _send_request(self, endpoint: str, bearer: bool = True):
        url = self.base_url + endpoint
        headers = {}
        if bearer:
            headers["Authorization"] = "Bearer " + self.token
        
        r = requests.get(url, headers=headers)
        r.raise_for_status() # Good practice to raise on error
        return r.json()

    def get_hackeps_event_id(self):
        return self._send_request("/v1/event/get_hackeps")["id"]

    def get_accepted_hackers(self):
        event_id = self.get_hackeps_event_id()
        return self._send_request(f'/v1/event/{event_id}/get_approved_hackers')

    def get_companies_by_tier(self, tier):
        return self._send_request(f'/v1/company/tier/{tier}/')
