import requests

class AqvifyAPI:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"x-api-key": self.api_key} if self.api_key else {}

    def get(self, endpoint, params=None):
        url = self.base_url + endpoint
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()
