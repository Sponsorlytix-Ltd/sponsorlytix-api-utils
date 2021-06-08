import os


class Development:
    def __init__(self):
        self.driver_user = ""
        self.driver_password = ""
        self.driver_host = ""
        self.driver_remote = False
        self.timeout = 2


class Production:
    def __init__(self):
        self.driver_user = "sponsorlytix"
        self.driver_password = "HXMswfgn7E7Y"
        self.driver_host = "3.16.155.212"
        self.driver_remote = True
        self.timeout = 2


def get_config():
    enviroment = os.environ.get('SPONSORLYTIX_ENV', 'dev').lower()
    configs = {
        'dev': Development,
        'prd': Production
    }
    return configs.get(enviroment, 'dev')()
