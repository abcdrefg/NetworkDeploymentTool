import tarfile

import docker
from UnitTestManager import UnitTestManager


class SandboxTestServer:

    __net_devices_json = "net_devices.json"

    def __init__(self, sandbox_server_name, ip_address):
        self.sandbox_server_name = sandbox_server_name
        self.client = docker.from_env()
        self.container = None

        for container in self.client.containers.list():
            self.container = container
        if self.container is None:
            raise Exception("Server container missing")
        self.unit_test_manager = UnitTestManager()
        for test_file in self.unit_test_manager.get_test_files():
            self.__copy_to(test_file, f'home/TestController/testcases')

        self.__set_ip_address(ip_address)
        self.__copy_to(self.__net_devices_json ,"f'home/TestController/")

    def __copy_to(self, src, dst):
        tar = tarfile.open(src + '.tar', mode='w')
        tar.add(src)
        tar.close()

        data = open(src + '.tar', 'rb').read()
        self.container.put_archive(dst, data)

    def __set_ip_address(self, ip_address):
        self.container.exec_run(f'ifconfig eth0 {ip_address}')

