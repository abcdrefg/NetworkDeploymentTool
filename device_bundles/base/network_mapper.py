import ipaddress

from device_bundles.base.bundle_config import BundleRegistry


class NetworkMapper:
    def __init__(self, db_connection):
        self._db_connection = db_connection
        self._devices_by_name = {}
        self._router_by_ip = {}
        self._connection_by_router = {}
        self._links = []
        self._nodes = []
        self._networks = []
        self._load_connections_from_db()

    def _load_connections_from_db(self):
        for device in self._db_connection.get_devices():
            self._devices_by_name[device["name"]] = device
            bundle = BundleRegistry.get_for_device(device)
            self._connection_by_router[device["name"]] = bundle.create_api_connection(
                bundle.api_auth(device["host"], device["secret"])
            )

    def _map_ips(self):
        for router_name, api_connection in self._connection_by_router.items():
            device = self._devices_by_name[router_name]
            bundle = BundleRegistry.get_for_device(device)
            interface_data = api_connection.get_interface_data()
            for interface_name, ip_address in bundle.parse_interface_ips(interface_data):
                self._router_by_ip[ip_address] = (router_name, interface_name)
        self._group_ips_by_subnet()

    def _group_ips_by_subnet(self):
        networks = {}

        for ip in self._router_by_ip:
            print(ip)
            network = ipaddress.IPv4Network(ip, strict=False)
            network_address = f"{network.network_address}/{network.netmask}"
            if network_address not in networks:
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
                if ipaddress.ip_address(possible_subnet.split("/")[0]) in ipaddress.ip_network(network_ip):
                    networks[network_ip].extend(networks[possible_subnet])
                    networks.pop(possible_subnet, None)
        self._networks = networks

    def _create_links(self, networks):
        self._create_nodes(networks.keys())
        for network in networks:
            for address in networks[network]:
                self._links.append(
                    (network, self._router_by_ip[address][0], self._router_by_ip[address][1])
                )

    def _create_nodes(self, networks):
        for network in networks:
            self._nodes.append(network)
        for router in self._connection_by_router:
            self._nodes.append(router)

    def generate_network_map(self):
        self._map_ips()
        self._create_links(self._networks)

    def get_nodes(self):
        return self._nodes

    def get_links(self):
        return self._links

    def get_routers(self):
        return list(self._connection_by_router.keys())

    def get_networks(self):
        return self._networks
