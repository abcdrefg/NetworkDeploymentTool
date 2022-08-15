from genie.testbed import load
from netmiko import ConnectHandler

commands = ['show inventory', 'show ip interface brief']


def load_devices():
    tb = load("devices.yaml")
    dev = tb.devices['ios1']
    dev.connect()
    dev.configure('''
        router ospf 1
        network 192.168.10.0 0.0.0.255 area 0
        no shutdown
    ''')
    # rip = Rip(instance_id='1')
    # rip.distance = 10
    # rip.maximum_paths = 15
    # dev.add_feature(rip)
    # rip.build_config(Apply = True)
    # for command in commands:
    # print(dev.parse(command))
    # ospf = Ospf(device = dev)
    # ospf.instance = '2'
    # ospf.area = '0'
    # ospf.enable = True
    # ospf.router_id = '0.0.0.0'
    # dev.add_feature(ospf)
    # ospf.build_config(apply=True)
    # interface = Interface(device=dev, name='FastEthernet1/0')
    # interface.ipv4='192.168.20.1'
    # interface.ipv4.netmask = '255.255.255.0'
    # interface.shutdown = False
    #
    # interface.build_config()


def create_connection():
    net_connect = ConnectHandler(device_type="cisco_ios_telnet", host="192.168.1.1", username="admin", password="admin1")
    net_connect.enable()
    config_command = ["router ospf 2", "network 192.168.100.0 0.0.0.255 area 0"]
    out = net_connect.send_config_set(config_command)
    print(out)
    print(net_connect.send_command("sh run"))


def check_connection(connection_wrapper):
    try:
        conn = ConnectHandler(device_type=connection_wrapper.device_type,
                              host=connection_wrapper.host,
                              username=connection_wrapper.username,
                              password=connection_wrapper.password,
                              secret=connection_wrapper.secret)
        conn.disconnect()
        return True
    except:
        return False

def get_running_config(connection_wrapper):
    conn = ConnectHandler(device_type=connection_wrapper.device_type,
                          host=connection_wrapper.host,
                          username=connection_wrapper.username,
                          password=connection_wrapper.password,
                          secret=connection_wrapper.secret)
    conn.enable()
    return conn.send_command("sh run")

def get_devices_running_confs(device_confs):
    running_configs = []
    for device_conf in device_confs:
        conn_wrapper = ConnectionWrapper(device_conf)
        running_configs.append(get_running_config(conn_wrapper))
    print(running_configs)
    return running_configs

class ConnectionWrapper:
    def __init__(self, device_dict):
        self.device_type = "cisco_ios_telnet"
        self.host = device_dict["host"]
        self.username = device_dict["username"]
        self.password = device_dict["password"]
        self.secret = device_dict["secret"]
        self.name = device_dict["name"]
