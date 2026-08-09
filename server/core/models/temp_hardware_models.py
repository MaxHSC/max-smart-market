class NewCabinet:
    def __init__(self, hardware_dict: dict):
        self.mac_address = hardware_dict["mac_address"]
        self.ip_address = hardware_dict["ip_address"]
        self.tcp_port = hardware_dict["tcp_port"]

class InstalledCabinet:
    def __init__(self, hardware_dict: dict):
        self.id = hardware_dict["cabinet_id"]
        self.shelf_capacity = hardware_dict["shelf_capacity"]
        self.current_installed_shelf = hardware_dict["current_installed_shelf"]
        self.mac_address = hardware_dict["mac_address"]
        self.ip_address = hardware_dict["ip_address"]
        self.tcp_port = hardware_dict["tcp_port"]


class NewShelf:
    def __init__(self, hardware_dict: dict):
        self.installed_cabinet_id = hardware_dict["isntalled_cabinet_id"]
        self.mac_address = hardware_dict["mac_address"]
        self.ip_address = hardware_dict["ip_address"]
        self.tcp_port = hardware_dict["tcp_port"]

class InstalledShelf:
    def __init__(self, hardware_dict: dict):
        self.id = hardware_dict["shelf_id"]
        self.installed_cabinet_id = hardware_dict["isntalled_cabinet_id"]
        self.weight_capacity_grams = hardware_dict["weight_capacity_grams"]
        self.volume_capacity = hardware_dict["volume_capacity"]
        self.current_weight_grams = hardware_dict["current_weight_grams"]
        self.current_volume = hardware_dict["current_volume"]
        self.mac_address = hardware_dict["mac_address"]
        self.ip_address = hardware_dict["ip_address"]
        self.tcp_port = hardware_dict["tcp_port"]