import os
from time import sleep

from bson.json_util import dumps

from server.core.DatabaseConnection import DatabaseConnection
from server.sandbox.Gns3Controller import Gns3Controller
from server.sandbox.Gns3VirtualNetworkJunctionSwitch import Gns3VirtualNetworkJunctionSwitch
from server.sandbox.SandboxInternalControllerConnection import SandboxInternalControllerConnection
from device_bundles import BundleRegistry
from device_bundles.base.network_mapper import NetworkMapper
import device_bundles  # noqa: F401 — register device bundles

class SandboxController:
    def __init__(self):
        self.__gns3_controller = Gns3Controller()
        self.__db_conn = DatabaseConnection()
        self.__devices_by_name = {d["name"]: d for d in self.__db_conn.get_devices()}
        self.__network_mapper = NetworkMapper(self.__db_conn)
        self.__network_switches = {}
        self.__routers = {}
        self.__routers_connection = {}
        self.__server_node = None
        self.__server_manager = None

    def create_sandbox(self):
        print('### Creating sandbox ###')
        self.__network_mapper.generate_network_map()
        print('### Map generated ###')
        networks = self.__network_mapper.get_networks().keys()
        self.create_junkction_switches(networks)
        print('### Junction switches created ###')
        self.create_routers(self.__network_mapper.get_routers())
        print('### Routers created ###')
        self.link_routers_with_networks()
        print('### Routers linked ###')
        self.create_test_server()
        print('### Server created ###')
        self.__gns3_controller.start_topo()
        sleep(30)

    def create_junkction_switches(self, networks):
        for network in networks:
            self.__network_switches[network] = Gns3VirtualNetworkJunctionSwitch(self.__gns3_controller.create_network_switch(network))

    def create_routers(self, routers):
        for router in routers:
            device = self.__devices_by_name[router]
            bundle = BundleRegistry.get_for_device(device)
            self.__routers[router] = self.__gns3_controller.create_router(router, bundle.gns3_template_name)

    def link_routers_with_networks(self):
        for link in self.__network_mapper.get_links():
            self.__gns3_controller.create_link_to_network(self.__network_switches[link[0]], self.__routers[link[1]], link[2])

    def create_test_server(self):
        self.__server_node = self.__gns3_controller.create_server_node()
        self.__gns3_controller.create_link_to_network(self.__network_switches[self.__db_conn.get_server_attachement_network()], self.__server_node, 'eth0')

    def write_configs_to_routers(self, configs_by_router_name):
        for router_id in configs_by_router_name:
            router = self.__routers[router_id]
            device = self.__devices_by_name[router_id]
            host = router.console_host
            if host == "0.0.0.0":
                host = self.__gns3_controller.get_gns3_host()
            conn = BundleRegistry.telnet_for_console(device, host, str(router.console))
            conn.load_config_commands(configs_by_router_name[router_id])

    def prepare_test_server(self):
        self.__create_net_devices_json_files()
        self.__server_manager = SandboxInternalControllerConnection(self.__db_conn.get_server_image_name(), self.__db_conn.get_server_ip_address(), 'localhost', 5011)
        try:
            os.remove("net_devices.json")
            os.remove("active_tests.json")
        except:
            pass

    def __create_net_devices_json_files(self):
        json_object = dumps(self.__db_conn.get_devices())
        with open("net_devices.json", "w") as outfile:
            outfile.write(json_object)
        json_object = dumps(self.__db_conn.get_active_tests())
        with open("active_tests.json", "w") as outfile:
            outfile.write(json_object)

    def execute_tests(self):
        return self.__server_manager.execute_tests()
