import tarfile

import docker
from UnitTestManager import UnitTestManager
import os
from telnetlib import Telnet
from time import sleep
import json
class SandboxTestServer:

    __net_devices_json = "net_devices.json"
    NUM_OF_POLLS = 10
    POLLS_TIMEOUT = 30
    current_poll = 0

    def __init__(self, sandbox_server_name, ip_address, telnet_host, telnet_port):
        self.sandbox_server_name = sandbox_server_name
        self.client = docker.from_env()
        self.container = None
        self.__telnet_connection = Telnet(telnet_host, telnet_port)

        for container in self.client.containers.list():
            self.container = container
        if self.container is None:
            raise Exception("Server container missing")
        self.unit_test_manager = UnitTestManager()
        for test_file in self.unit_test_manager.get_test_files():
            self.__copy_to(test_file, f'home/TestController/')

        self.__set_ip_address(ip_address)
        self.__copy_to(self.__net_devices_json, f'home/TestController')

    def __copy_to(self, src, dst):
        tar = tarfile.open(src + '.tar', mode='w')
        tar.add(src)
        tar.close()
        data = open(src + '.tar', 'rb').read()
        self.container.put_archive(dst, data)
        os.remove(src + '.tar')

    def __set_ip_address(self, ip_address):
        self.container.exec_run(f'ifconfig eth0 {ip_address}')

    def execute_tests(self):
        self.__telnet_connection.write(b"cd /home/TestController \n")
        self.__telnet_connection.write(b"source controller_env/bin/activate \n")
        self.__telnet_connection.write(b"python3 UnitTestController.py \n")
        return self.__poll_for_results()

    def __poll_for_results(self):
        current_poll =+ 1
        try:
            results = self.container.exec_run(f'cat /home/TestController/test_results.json').output.decode("utf-8")
            return json.loads(results)
        except:
            if current_poll >= self.NUM_OF_POLLS:
                return []
            sleep(self.POLLS_TIMEOUT)
            self.__poll_for_results()