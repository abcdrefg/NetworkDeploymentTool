class CommandLineAuthData:

    def __init__(self, host, username, password):
        self.port = 22
        self.host = host
        self.username = username
        self.password = password
        self.device_type = 'vyos'

class ApiAuthData:

    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key