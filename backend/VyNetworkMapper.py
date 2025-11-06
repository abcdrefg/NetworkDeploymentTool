
from DatabaseConnection import DatabaseConnection
from VyRouterAuthData import ApiAuthData
from VyAPIConnection import VyAPIConnection
import ipaddress

class VyNetworkMapper:
    __router_by_ip = {}
    __connection_by_router = {}
    __links = []
    __nodes = []
    __networks = []

    def __init__(self, db_connection:DatabaseConnection):
        self.__db_connection = db_connection
        self.__get_connection_credentials_from_db()

    def __get_connection_credentials_from_db(self):
        for credentials in self.__db_connection.get_devices():
            self.__connection_by_router[credentials['name']] = VyAPIConnection(ApiAuthData(credentials['host'], credentials['secret']))

    def __map_ips(self):
        for router_name in self.__connection_by_router:
            ip_list = self.__get_ip_from_output(self.__connection_by_router[router_name].get_interface_data())
            for ip_port_address in ip_list:
                self.__router_by_ip[ip_port_address[1]] = (router_name, ip_port_address[0])
        self.__group_ips_by_subnet()

    def __get_ip_from_output(self, output):
        lines = output.split('\n')
        ip_address = []
        for line in lines:
            if not line.startswith('eth'):
                continue
            columns = line.split()
            ip_address.append((columns[0],columns[1]))
        return ip_address

    def __group_ips_by_subnet(self):
        networks = {}

        for ip in self.__router_by_ip:
            network_address = f'{ipaddress.IPv4Network(ip, strict=False).network_address}/{ipaddress.IPv4Network(ip, strict=False).netmask}'
            if not network_address in networks:
                networks[network_address] = []
            networks[network_address].append(ip)

        networks_copy = networks.copy()

        for network_ip in networks_copy:
            if network_ip not in networks:
                continue
            for possible_subnet in networks_copy:
                if network_ip is possible_subnet:
                    continue
                if possible_subnet not in networks:
                    continue
                if ipaddress.ip_address(possible_subnet.split('/')[0]) in ipaddress.ip_network(network_ip):
                    networks[network_ip].extend(networks[possible_subnet])
                    networks.pop(possible_subnet, None)
        self.__networks = networks


    def __create_links(self, networks):
        self.__create_nodes(networks.keys())
        for network in networks:
            for address in networks[network]:
                self.__links.append((network,self.__router_by_ip[address][0], self.__router_by_ip[address][1]))

    def __create_nodes(self, networks):
        for network in networks:
            self.__nodes.append(network)
        for router in self.__connection_by_router:
            self.__nodes.append(router)

    def generate_network_map(self):
        self.__map_ips()
        self.__create_links(self.__networks)

    def get_nodes(self):
        return self.__nodes

    def get_links(self):
        return self.__links

    def get_routers(self):
        routers = []
        for router_id in self.__connection_by_router:
            routers.append(router_id)
        return routers

    def get_networks(self):
        return self.__networks
