import json

import requests

from device_bundles.base.api_connection import APIConnection
from device_bundles.vyos.router_auth import VyosApiAuthData


class VyosAPIConnection(APIConnection):
    SHOW_ENDPOINT = "/show"
    REQUEST_FAILED = "Request failed"

    def __init__(self, credentials: VyosApiAuthData):
        super().__init__(credentials)

    def get_interface_data(self):
        response = json.loads(
            self.make_request("show", self.SHOW_ENDPOINT, ["interfaces"]).text
        )
        if not response["success"]:
            raise Exception(f"{self.REQUEST_FAILED} {response['data']}")
        return response["data"]

    def make_request(self, action, endpoint, path):
        url = f"https://{self.credentials.host}{endpoint}"
        data = {"op": action, "path": path}
        payload = {"data": json.dumps(data), "key": self.credentials.api_key}
        return requests.request("POST", url, headers={}, data=payload, verify=False)
