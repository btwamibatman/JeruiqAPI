import requests

class OverpassClient:
    def __init__(self, base_url="https://overpass-api.de/api/interpreter"):
        self.base_url = base_url

    def query(self, overpass_query: str):
        """
        Send a raw Overpass QL query and return the JSON response.
        """
        response = requests.post(self.base_url, data={"data": overpass_query})
        response.raise_for_status()
        return response.json()