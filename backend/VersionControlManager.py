from DatabaseConnection import DatabaseConnection
from DeviceLoader import get_devices_running_confs
from datetime import datetime
import difflib
import io
import re

class VersionControlManager:

    def generate_config(self, is_current_config):
        database_conn = DatabaseConnection()
        device_conf_list = get_devices_running_confs(database_conn.get_devices())
        devices_configs_map = {}
        for device_conf_wrapper in device_conf_list:
            devices_configs_map[device_conf_wrapper["name"]] = device_conf_wrapper["config"]
        version_control_object = {}
        version_control_object["configs"] = devices_configs_map
        version_control_object["timestamp"] = datetime.now()
        database_conn.insert_config_version(version_control_object, is_current_config)

    def generate_diff_with_current_config(self):
        database_conn = DatabaseConnection()
        running_device_conf_list = get_devices_running_confs(database_conn.get_devices())
        running_devices_configs_map = {}
        for device_conf_wrapper in running_device_conf_list:
            running_devices_configs_map[device_conf_wrapper["name"]] = device_conf_wrapper["config"]
        try:
            curr_devices_configs_map = database_conn.get_current_configs()
        except:
            self.generate_config(True)
            curr_devices_configs_map = database_conn.get_current_configs()
        return self.diffrences_generator(curr_devices_configs_map, running_devices_configs_map)

    def generate_diff_from_spec_conf(self, version_id):
        database_conn = DatabaseConnection()
        running_device_conf_list = get_devices_running_confs(database_conn.get_devices())
        running_devices_configs_map = {}
        for device_conf_wrapper in running_device_conf_list:
            running_devices_configs_map[device_conf_wrapper["name"]] = device_conf_wrapper["config"]
        curr_devices_configs_map = database_conn.get_config_version_by_id(version_id)
        return self.diffrences_generator(curr_devices_configs_map, running_devices_configs_map)

    def diffrences_generator(self, curr_devices_configs_map, running_devices_configs_map):
        config_diffs = {}
        for device_name in running_devices_configs_map.keys():
            old_string = ''  # null pointer preventing
            new_string = ''
            if device_name in curr_devices_configs_map:
                old_string = curr_devices_configs_map[device_name]
            if device_name in running_devices_configs_map:
                new_string = running_devices_configs_map[device_name]
            old = io.StringIO(old_string)
            new = io.StringIO(new_string)
            config_diffs[device_name] = difflib.HtmlDiff(wrapcolumn=50).make_table(old.readlines()[3:], new.readlines()[3:], context=True)
        return config_diffs