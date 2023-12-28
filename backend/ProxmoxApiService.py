from proxmoxer import ProxmoxAPI

class ProxmoxApiService:

    __node_name = 'pve'
    __DEFAULT_STARTING_NUMBER = 2000

    def set_host(self, host):
        self.__host = host
        return self

    def set_credentials(self, user, password):
        self.__user = user
        self.__password = password
        return self

    def create_connection(self):
        if self.__user is None or self.__host is None:
            raise Exception('Cannot create connection, set host and credentials')
        self.__ProxmoxAPI = ProxmoxAPI(self.__host, user=f'{self.__user}@pam', password=self.__password, verify_ssl = False)
        return self

    def create_router_vm(self):
        for node in self.__ProxmoxAPI.nodes.get():
            print(node)
            for vm in self.__ProxmoxAPI.nodes(node["node"]).qemu.get():
                print(f"{vm['vmid']}. {vm['name']} => {vm['status']}")
            for net in self.__ProxmoxAPI.nodes(node["node"]).network.get():
                print(net)

    def create_networks(self, networks_to_create):
        virtual_network_by_real_network = {}
        iteration = self.__DEFAULT_STARTING_NUMBER
        for network in networks_to_create:
            self.__ProxmoxAPI.nodes(self.__node_name).network.post(iface=f'vmbr{iteration}', node=self.__node_name,
                                                                   type='bridge')
            virtual_network_by_real_network[network] = f'vmbr{iteration}'
            iteration += 1
        return virtual_network_by_real_network
