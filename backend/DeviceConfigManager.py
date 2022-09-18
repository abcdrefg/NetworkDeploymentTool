from DatabaseConnection import DatabaseConnection
from netmiko import ConnectHandler
from DeviceLoader import ConnectionWrapper

class DeviceConfigManager:

    configs_by_name = {}
    device_conn_by_name = {}

    def __init__(self):
        self.get_configs()
        self.get_conn_confs()

    def get_conn_confs(self):
        database_conn = DatabaseConnection()
        self.device_conn_by_name = database_conn.get_device_connection_configs_map()

    def get_configs(self):
        database_conn = DatabaseConnection()
        self.configs_by_name = database_conn.get_configs_to_send_by_device_name()

    def test_configs(self):
        error_array = []
        for device_name in self.configs_by_name.keys():
            connection_wrapper = self.device_conn_by_name[device_name]
            conn = ConnectHandler(device_type=connection_wrapper.os,
                                  host=connection_wrapper.host,
                                  username=connection_wrapper.username,
                                  password=connection_wrapper.password,
                                  secret=connection_wrapper.secret)
            conn.enable()
            conn.config_mode()
            commands_to_execute = self.parse_configs(self.configs_by_name[device_name])
            errors = ''
            running_conf = conn.send_command('do sh run')
            running_conf = running_conf.split('\n')[3:]
            for command_groups in commands_to_execute:
                output = conn.send_config_set(command_groups)
                if 'Invalid input' in output:
                    errors += 'Error during executing: '.join(command_groups) + '\n' + 'Error: ' + output
            conn.send_config_set(running_conf, read_timeout=120)
            conn.disconnect()
            if len(errors) > 0:
                error_dict = {}
                error_dict['device'] = device_name
                error_dict['errors'] = errors
                error_array.append(error_dict)
        return error_array

    def deploy_config(self):
        rollback_map = {}
        for device_name in self.configs_by_name.keys():
            connection_wrapper = self.device_conn_by_name[device_name]
            conn = ConnectHandler(device_type=connection_wrapper.os,
                                  host=connection_wrapper.host,
                                  username=connection_wrapper.username,
                                  password=connection_wrapper.password,
                                  secret=connection_wrapper.secret)
            conn.enable()
            conn.config_mode()
            commands_to_execute = self.parse_configs(self.configs_by_name[device_name])
            errors = ''
            running_conf = conn.send_command('do sh run')
            rollback_map[device_name] = running_conf.split('\n')[3:]
            for command_groups in commands_to_execute:
                output = conn.send_config_set(command_groups)
                if 'Invalid input' in output:
                    errors += 'Error during executing ' + device_name + ' config: ' .join(command_groups) + '\n' + 'Error: ' + output
            conn.disconnect()
            if len(errors) != 0:
                self.rollback_configs(rollback_map)
                return errors
        return 'success'

    def rollback_configs(self, rollback_map):
        for device_name in rollback_map:
            connection_wrapper = self.device_conn_by_name[device_name]
            conn = ConnectHandler(device_type=connection_wrapper.os,
                                  host=connection_wrapper.host,
                                  username=connection_wrapper.username,
                                  password=connection_wrapper.password,
                                  secret=connection_wrapper.secret)
            conn.enable()
            conn.config_mode()
            conn.send_config_set(rollback_map[device_name], read_timeout=120)
            conn.disconnect()

    def parse_configs(self, commands_string):
        commands_list = commands_string.split("\n\n")
        commands_parsed = []
        for commands in commands_list:
            command_group = commands.split("\n")
            if "" in command_group:
                command_group.remove("")
            commands_parsed.append(command_group)
        return commands_parsed