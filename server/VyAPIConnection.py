import requests
from VyRouterAuthData import ApiAuthData
import json

class VyAPIConnection:

    RETRIEVE_ENDPOINT = '/retrieve'
    SHOW_ENDPOINT = '/show'

    REQUEST_FAILED = 'Request failed'

    def __init__(self, apiAuthCredentials: ApiAuthData):
        self.credentials = apiAuthCredentials

    def get_interface_data(self):
        response = json.loads(self.make_request('show', self.SHOW_ENDPOINT, ['interfaces']).text)
        if not response['success']:
            raise Exception(f'{self.REQUEST_FAILED} {response["data"]}')
        return response["data"]

    def get_eth_ints(self):
        lines = self.get_interface_data().split('\n')
        eth_ints = []
        for line in lines:
            if not line.startswith('eth'):
                continue
            columns = line.split()
            eth_ints.append(columns[0])
        return eth_ints

    def make_request(self, action, endpoint, path):
        url = f'https://{self.credentials.host}{endpoint}'
        data = {}
        data['op'] = action
        data['path'] = path
        payload = {'data': json.dumps(data),'key': self.credentials.api_key}
        return requests.request("POST", url, headers={}, data=payload, verify=False)

