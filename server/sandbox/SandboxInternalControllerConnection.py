import json
import os
import tarfile
from time import sleep

import docker
import glob

DEFAULT_DOCKER_URL = 'tcp://192.168.18.32:2375'


class SandboxInternalControllerConnection:
    __net_devices_json = "net_devices.json"
    NUM_OF_POLLS = 3
    POLLS_TIMEOUT = 30
    current_poll = 0
    COMMAND_TIMEOUT = 0.05

    def __init__(self, sandbox_server_name, ip_address, telnet_host, telnet_port):
        self.sandbox_server_name = sandbox_server_name
        docker_host = os.environ.get('DOCKER_HOST', DEFAULT_DOCKER_URL)
        self.client = docker.DockerClient(base_url=docker_host)
        self.container = None
        for container in self.client.containers.list():
            if "Testserver" in container.name:
                self.container = container
                break
        if self.container is None:
            raise Exception("Server container missing")
        for test_file in self.__get_test_files():
            self.__copy_to(test_file, f'/home/TestController/')

        self.__set_ip_address(ip_address)
        self.__copy_to(self.__net_devices_json, f'/home/TestController')
        self.__copy_to('active_tests.json', f'/home/TestController')

    def __get_test_files(self):
        return glob.glob("testcases/*.py")

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
        self.container.exec_run(['/bin/bash', '/home/TestController/test_exec.sh'])
        return self.__poll_for_results(0)

    def __poll_for_results(self, current_poll):
        current_poll += 1
        try:
            results = self.container.exec_run(f'cat /home/TestController/test_results.json').output.decode("utf-8")
            return json.loads(results)
        except Exception:
            if current_poll >= self.NUM_OF_POLLS:
                return []
            sleep(self.POLLS_TIMEOUT)
            return self.__poll_for_results(current_poll)
