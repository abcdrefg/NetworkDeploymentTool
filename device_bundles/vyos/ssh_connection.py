from netmiko import ConnectHandler

from device_bundles.base.ssh_connection import SSHConnection
from device_bundles.vyos.router_auth import VyosCommandLineAuthData


class VyosSSHConnection(SSHConnection):
    SHOW_CONFIG_COMMAND = "show config commands"
    COMMAND_FAILURE_SUBSTRING = "failed"

    def __init__(self, credentials: VyosCommandLineAuthData):
        super().__init__(credentials)
        self.connection = ConnectHandler(
            device_type=credentials.device_type,
            host=credentials.host,
            username=credentials.username,
            password=credentials.password,
            port=credentials.port,
        )

    def get_config_as_commands(self):
        return self.connection.send_command(self.SHOW_CONFIG_COMMAND)

    def send_command_set(self, commands):
        commands_parsed = commands.split("\n")
        errors = []
        self.connection.config_mode()
        for command in commands_parsed:
            try:
                output = self.connection.send_command(command)
                if self.COMMAND_FAILURE_SUBSTRING in output:
                    errors.append(output)
            except Exception as e:
                errors.append(e.args)
        return errors

    def check_connection(self):
        try:
            self.connection.send_command(self.SHOW_CONFIG_COMMAND)
        except Exception:
            return False
        return True

    def rollback(self):
        self.connection.send_command("rollback")

    def commit(self):
        self.connection.send_command("commit")

    def save(self):
        self.connection.send_command("save")
