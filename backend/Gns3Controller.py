import gns3fy
from time import sleep
TESTBED_SERVER_NAME = 'sandbox-server'
VYOS_TEMPLATE_NAME = 'VyOs'
ETHERNET_SWITCH = 'Ethernet switch'


class Gns3Controller:

    __project_id = ''
    __project = None
    __gns3_server = None
    def __init__(self):
        self.__gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
        project = gns3fy.Project(name='MgrMain', connector=self.__gns3_server)
        try:
            project.get()
            project_to_delete_id = project.project_id
            self.__gns3_server.delete_project(project_to_delete_id)
        except:
            print('Project does not exist')
        self.__gns3_server.create_project(name='MgrMain')
        self.__project = gns3fy.Project(name='MgrMain', connector=self.__gns3_server)
        self.__project.get()
        self.__project_id = self.__project.project_id

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






