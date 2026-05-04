class Gns3VirtualNetworkJunctionSwitch:

    def __init__(self, gns3Switch):
        self.__switch = gns3Switch
        self.__free_ports = gns3Switch.ports

    def get_switch(self):
        return self.__switch

    def next_port(self):
        return self.__free_ports.pop()