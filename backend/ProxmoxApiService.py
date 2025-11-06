from proxmoxer import ProxmoxAPI

class ProxmoxApiService:

    __node_name = 'pve'
    __DEFAULT_STARTING_NUMBER = 2000
    __networks_dict = {}
    __last_vmid = 2000

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

    def create_router_vm(self, number_of_eth_ports):
        self.__ProxmoxAPI.nodes(self.__node_name).qemu.post(node=self.__node_name, vmid=self.__last_vmid, ostype='l26', memory=1100, scsi0="local-lvm:10", ide0="local:iso/vyos-1.5-rolling-202311261237-amd64.iso,media=cdrom", net0="model=virtio,bridge=vmbr2000", net1="model=virtio,bridge=vmbr2001")
        self.__last_vmid += 1

    def create_networks(self, networks_to_create):
        virtual_network_by_real_network = {}
        iteration = self.__DEFAULT_STARTING_NUMBER
        for network in networks_to_create:
            self.__ProxmoxAPI.nodes(self.__node_name).network.post(iface=f'vmbr{iteration}', node=self.__node_name,
                                                                   type='bridge')
            virtual_network_by_real_network[network] = f'vmbr{iteration}'
            iteration += 1
        self.__networks_dict = virtual_network_by_real_network
        return virtual_network_by_real_network

    def get_networks(self):
        return self.__networks_dict
