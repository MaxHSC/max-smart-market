from server.database import hardware_dao as hard_dao
from server.core.models import temp_hardware_models as hard_mod
from server.core.validators import hardware_validators as hard_val

class HardwareServices:
    def __init__(self):
        self.cabinet_dict = {}
        self.action_mapping = {
            "INSTALL_NEW_CABINET": self.install_new_cabinet,
            "INSTALL_NEW_SHELF": self.install_new_shelf,
            "GET_CABINET_INFO": self.get_cabinet_info,
            "GET_SHELF_INFO": self.get_shelf_info,
        }
    
    def process_payload(self, payload: dict) -> bool:
        validation_result = hard_val.payload_validation(payload)

        if not validation_result:
            return False
        
        #inserir lógica de autenticação

        payload_action = payload["header"]["action"]

        action_target = self.action_mapping[payload_action]

        header = payload["header"]
        payload = payload["payload"]

        action_result = action_target(header,payload)

        return action_result


    def attributes_to_dict(self,self_object, fields: list[str]) -> dict:
        object_dict = {}

        for field in fields:
            object_dict[field] = getattr(self_object,field)
        
        return object_dict


    def install_new_cabinet(self,header:dict,payload:dict) -> bool:
        new_cabinet_object: hard_mod.NewCabinet = hard_mod.NewCabinet(payload)

        attributes_fields = ["hardware_mac_address", "hardware_tcp_port"]

        new_cabinet_dict = self.attributes_to_dict(new_cabinet_object, attributes_fields)

        result = hard_dao.add_new_cabinet(new_cabinet_dict)

        return result


    def get_cabinet_info(self,header:dict,payload:dict) -> hard_mod.InstalledCabinet | None:
        cabinet_info: dict = hard_dao.get_cabinet_info(payload["installed_cabinet_id"])

        if not cabinet_info:
            return None

        cabinet_object: hard_mod.InstalledCabinet = hard_mod.InstalledCabinet(cabinet_info)

        return cabinet_object


    def install_new_shelf(self,header:dict,payload:dict) -> bool:
        cabinet_object: hard_mod.InstalledCabinet | None = self.get_cabinet_info(header,payload)

        if cabinet_object is None:
            return False

        if cabinet_object.current_installed_shelf + 1 > cabinet_object.shelf_capacity:
            return False
        
        new_shelf_object: hard_mod.NewShelf = hard_mod.NewShelf(payload)

        attributes_fields = ["isntalled_cabinet_id","hardware_mac_address", "hardware_tcp_port"]

        new_shelf_dict = self.attributes_to_dict(new_shelf_object, attributes_fields)

        result = hard_dao.add_new_shelf(new_shelf_dict,cabinet_object.id)

        return result


    def get_shelf_info(self,header:dict,payload:dict) -> hard_mod.InstalledShelf | dict:
        shelf_info: dict = hard_dao.get_shelf_info(payload["shelf_id"])

        if not shelf_info:
            return shelf_info

        shelf_object: hard_mod.InstalledShelf = hard_mod.InstalledShelf(shelf_info)

        return shelf_object
        

sample_payload = {
    "header":
    {
        "correlation_id": "req_8f3a9b1c-2026",
        "client_type": "totem",
        "client_id": "TOTEM_LOJA_01",
        "user_id": "3",
        "role": "employee", #consumer, employee, manager
        "auth_token": "bearer.jwt.token.here",
        "action": "INSTALL_NEW_CABINET", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO
        "timestamp": "1785816136"
    },
    "payload":
    {
        "hardware_mac_address": "xx:xx:xx:xx:xx",
        "hardware_tcp_port": "80001",
        "hardware_current_ip_address": "192.168.1.245"
    },
}