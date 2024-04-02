from netmiko import ConnectHandler
from VyRouterAuthData import CommandLineAuthData

class VySSHConnection:

    def __init__(self, credentials: CommandLineAuthData):
        self.credentials = credentials
        self.connection = ConnectHandler(**{
          "device_type": credentials.device_type,
          "host": credentials.host,
          "username": credentials.username,
          "password": credentials.password,
          "port": credentials.port,
        })

    def get_config_as_commands(self):
        output = self.connection.send_command('show config commands')
        return output

    def send_command_set(self, commands):
        commands_parsed = commands.split("\n")
        errors = []
        self.connection.config_mode()
        for command in commands_parsed:
            try:
                output = self.connection.send_command(command)
                if 'failed' in output:
                    errors.append(output)
            except Exception as e:
                errors.append(e.args)
        return errors

    def check_connection(self):
        try:
            self.connection.send_command('show config commands')
        except:
            return False
        return True

    def rollback(self):
        print(self.connection.send_command('rollback'))