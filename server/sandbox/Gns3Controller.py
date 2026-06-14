import os

import gns3fy

# Monkeypatch gns3fy to remove Pydantic internal fields from GNS3 REST API payloads.
# Under Python 3.12 and Pydantic v2, __dict__ of gns3fy objects includes '__pydantic_initialised__'.
# When passed to GNS3, the server rejects the request with a 400 JSON schema validation error.
def _clean_pydantic_fields(data):
    if isinstance(data, dict):
        return {
            k: _clean_pydantic_fields(v)
            for k, v in data.items()
            if not k.startswith("__pydantic") and k != "__initialised__"
        }
    elif isinstance(data, list):
        return [_clean_pydantic_fields(item) for item in data]
    return data

_original_http_call = gns3fy.Gns3Connector.http_call

def _patched_http_call(self, method, url, data=None, json_data=None, headers=None, verify=False, params=None):
    if json_data is not None:
        json_data = _clean_pydantic_fields(json_data)
    return _original_http_call(self, method, url, data=data, json_data=json_data, headers=headers, verify=verify, params=params)

gns3fy.Gns3Connector.http_call = _patched_http_call

import requests
from time import sleep

TESTBED_SERVER_NAME = 'sandbox-server'
ETHERNET_SWITCH = 'Ethernet switch'
DEFAULT_GNS3_URL = 'http://192.168.18.32:3080'


class Gns3ConnectionError(Exception):
    pass


class Gns3Controller:
    __project_id = ''
    __project = None
    __gns3_server = None

    def __init__(self):
        url = os.environ.get('GNS3_URL', DEFAULT_GNS3_URL)
        user = os.environ.get('GNS3_USER', 'admin')
        password = os.environ.get('GNS3_PASSWORD', 'admin')

        if not user or not password:
            raise Gns3ConnectionError(
                'GNS3 API requires authentication. Set GNS3_USER and GNS3_PASSWORD '
                'to your GNS3 server credentials (GNS3 → Preferences → Server), '
                'then restart the Flask server.'
            )

        self.__gns3_server = gns3fy.Gns3Connector(url, user=user, cred=password)
        self.__verify_connection(url)

        project = gns3fy.Project(name='sandbox-deployment', connector=self.__gns3_server)
        try:
            project.get()
            self.__gns3_server.delete_project(project.project_id)
        except Exception:
            print('Project does not exist')
        try:
            self.__gns3_server.create_project(name='sandbox-deployment')
        except requests.HTTPError as exc:
            raise Gns3ConnectionError(f'Failed to create GNS3 project sandbox-deployment: {exc}') from exc
        self.__project = gns3fy.Project(name='sandbox-deployment', connector=self.__gns3_server)
        self.__project.get()
        self.__project_id = self.__project.project_id

    def __verify_connection(self, url):
        try:
            self.__gns3_server.get_version()
        except requests.JSONDecodeError as exc:
            raise Gns3ConnectionError(
                'GNS3 rejected the credentials in GNS3_USER / GNS3_PASSWORD.'
            ) from exc
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 401:
                raise Gns3ConnectionError(
                    'GNS3 rejected the credentials in GNS3_USER / GNS3_PASSWORD.'
                ) from exc
            raise Gns3ConnectionError(
                f'Cannot reach GNS3 at {url} (HTTP {exc.response.status_code if exc.response else "error"}).'
            ) from exc
        except requests.RequestException as exc:
            raise Gns3ConnectionError(
                f'Cannot reach GNS3 at {url}. Start the GNS3 server and confirm GNS3_URL ({exc}).'
            ) from exc

    def create_node(self, name, template):
        node = gns3fy.Node()
        node.project_id = self.__project_id
        node.connector = self.__gns3_server
        node.template = template
        node.name = name
        node.create()
        return node

    def create_network_switch(self, network):
        return self.create_node(network, ETHERNET_SWITCH)

    def create_router(self, name, template):
        return self.create_node(name, template)

    def create_server_node(self):
        return self.create_node('Test server', TESTBED_SERVER_NAME)

    def create_link_to_network(self, network_switch, router, router_port):
        self.__project.get()
        self.__project.create_link(network_switch.get_switch().name, network_switch.next_port()['name'], router.name, router_port)

    def start_topo(self):
        self.__project.get()
        sleep(1)
        self.__project.start_nodes()
        sleep(5)

    def get_gns3_host(self):
        from urllib.parse import urlparse
        url = os.environ.get('GNS3_URL', DEFAULT_GNS3_URL)
        return urlparse(url).hostname or 'localhost'
