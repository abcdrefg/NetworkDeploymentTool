import os
import tarfile

import docker
from UnitTestManager import UnitTestManager

class SandboxTestServer:


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
            self.copy_to(test_file, f'home/')

        self.container.exec_run(f'ifconfig eth0 {ip_address}')

    def copy_to(self, src, dst):
        tar = tarfile.open(src + '.tar', mode='w')
        tar.add(src)
        tar.close()

        data = open(src + '.tar', 'rb').read()
        self.container.put_archive(dst, data)