class NewCabinet:
    def __init__(self, hardware: dict):
        self.mac_address = hardware["hardware_mac_address"]
        self.ip_address = hardware["hardware_ip_address"]
        self.tcp_port = hardware["hardware_tcp_port"]

class InstalledCabinet:
    def __init__(self, hardware: dict):
        self.id = hardware["id"]
        self.shelf_capacity = hardware["shelf_capacity"]
        self.current_installed_shelf = hardware["current_installed_shelf"]
        self.mac_address = hardware["hardware_mac_address"]
        self.ip_address = hardware["hardware_ip_address"]
        self.tcp_port = hardware["hardware_tcp_port"]


class NewShelf:
    def __init__(self, hardware: dict):
        self.installed_cabinet_id = hardware["isntalled_cabinet_id"]
        self.mac_address = hardware["hardware_mac_address"]
        self.ip_address = hardware["hardware_ip_address"]
        self.tcp_port = hardware["hardware_tcp_port"]

class InstalledShelf:
    def __init__(self, hardware: dict):
        self.id = hardware["id"]
        self.installed_cabinet_id = hardware["isntalled_cabinet_id"]
        self.weight_capacity_grams = hardware["weight_capacity_grams"]
        self.volume_capacity = hardware["volume_capacity"]
        self.current_weight_grams = hardware["current_weight_grams"]
        self.current_volume = hardware["current_volume"]
        self.mac_address = hardware["hardware_mac_address"]
        self.ip_address = hardware["hardware_ip_address"]
        self.tcp_port = hardware["hardware_tcp_port"]