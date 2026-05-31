import os

import gns3fy
import requests
from time import sleep

TESTBED_SERVER_NAME = 'sandbox-server'
VYOS_TEMPLATE_NAME = 'VyOs'
ETHERNET_SWITCH = 'Ethernet switch'
DEFAULT_GNS3_URL = 'http://localhost:3080'


class Gns3ConnectionError(Exception):
    pass


class Gns3Controller:
    __project_id = ''
    __project = None
    __gns3_server = None

    def __init__(self):
        url = os.environ.get('GNS3_URL', DEFAULT_GNS3_URL)
        user = os.environ.get('GNS3_USER')
        password = os.environ.get('GNS3_PASSWORD')

        if not user or not password:
            raise Gns3ConnectionError(
                'GNS3 API requires authentication. Set GNS3_USER and GNS3_PASSWORD '
                'to your GNS3 server credentials (GNS3 → Preferences → Server), '
                'then restart the Flask server.'
            )

        self.__gns3_server = gns3fy.Gns3Connector(url, user=user, cred=password)
        self.__verify_connection(url)

        project = gns3fy.Project(name='MgrMain', connector=self.__gns3_server)
        try:
            project.get()
            self.__gns3_server.delete_project(project.project_id)
        except Exception:
            print('Project does not exist')
        try:
            self.__gns3_server.create_project(name='MgrMain')
        except requests.HTTPError as exc:
            raise Gns3ConnectionError(f'Failed to create GNS3 project MgrMain: {exc}') from exc
        self.__project = gns3fy.Project(name='MgrMain', connector=self.__gns3_server)
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

    def create_vyos_router(self, name):
        return self.create_node(name, VYOS_TEMPLATE_NAME)

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
