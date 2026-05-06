from core.DatabaseConnection import DatabaseConnection
from device_bundles.vyos.VySSHConnection import VySSHConnection
from device_bundles.vyos.VyRouterAuthData import CommandLineAuthData


class DeviceConfigManager:
    configs_by_name = {}
    device_conn_by_name = {}

    def __init__(self):
        self.get_configs()

    def get_configs(self):
        database_conn = DatabaseConnection()
        self.configs_by_name = database_conn.get_configs_to_send_by_device_name()

    def test_configs(self):
        errors = self.deploy_test_config()
        return errors

    def deploy_config(self):
        error_array = []
        connections = []
        for device in DatabaseConnection().get_devices():
            commands = self.configs_by_name[device["name"]]
            connection = VySSHConnection(CommandLineAuthData(device["host"], device["username"], device["password"]))
            connections.append(connection)
            errors = connection.send_command_set(commands)
            if len(errors) > 0:
                error_dict = {}
                error_dict['device'] = device["name"]
                error_dict['errors'] = errors
                error_array.append(error_dict)
        if len(error_array) > 0:
            return error_array
        for conn in connections:
            conn.commit()
            conn.save()
        return 'success'

    def deploy_test_config(self):
        error_array = []
        for device in DatabaseConnection().get_devices():
            commands = self.configs_by_name[device["name"]]
            connection = VySSHConnection(CommandLineAuthData(device["host"], device["username"], device["password"]))
            errors = connection.send_command_set(commands)
            if len(errors) > 0:
                error_dict = {}
                error_dict['device'] = device["name"]
                error_dict['errors'] = errors
                error_array.append(error_dict)
            connection.rollback()
        return error_array
