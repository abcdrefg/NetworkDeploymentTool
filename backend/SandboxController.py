from Gns3Controller import Gns3Controller
from VyNetworkMapper import VyNetworkMapper
from DatabaseConnection import DatabaseConnection
from Gns3VirtualNetworkJunctionSwitch import Gns3VirtualNetworkJunctionSwitch
from VyRouterAuthData import CommandLineAuthData
from VyTelnetConnection import VyTelnetConnection
from time import sleep
class SandboxController:

    def __init__(self):
        self.__gns3_controller = Gns3Controller()
        self.__db_conn = DatabaseConnection()
        self.__network_mapper = VyNetworkMapper(self.__db_conn)
        self.__network_switches = {}
        self.__routers = {}
        self.__routers_connection = {}
        self.__server = None

    def create_sandbox(self):
        self.__network_mapper.generate_network_map()
        networks = self.__network_mapper.get_networks().keys()
        self.create_junkction_switches(networks)
        self.create_routers(self.__network_mapper.get_routers())
        self.link_routers_with_networks()
        self.create_test_server()
        self.__gns3_controller.start_topo()
        sleep(30)
        #self.__start_routers()

    def create_junkction_switches(self, networks):
        for network in networks:
            self.__network_switches[network] = Gns3VirtualNetworkJunctionSwitch(self.__gns3_controller.create_network_switch(network))

    def create_routers(self, routers):
        for router in routers:
            self.__routers[router] = self.__gns3_controller.create_vyos_router(router)

    def link_routers_with_networks(self):
        for link in self.__network_mapper.get_links():
            self.__gns3_controller.create_link_to_network(self.__network_switches[link[0]], self.__routers[link[1]], link[2])

    def create_test_server(self):
        self.__server = self.__gns3_controller.create_server_node()
        self.__gns3_controller.create_link_to_network(self.__network_switches[self.__db_conn.get_server_attachement_network()], self.__server, 'eth0')

    def __start_routers(self):
        for router_id in self.__routers:
            self.__routers[router_id].start()

    def write_configs_to_routers(self, configs_by_router_name):
        for router_id in configs_by_router_name:
            router = self.__routers[router_id]
            VyTelnetConnection(CommandLineAuthData(router.console_host, 'vyos', 'vyos', str(router.console))).load_config_commands(configs_by_router_name[router_id])


