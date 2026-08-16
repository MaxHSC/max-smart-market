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

        if cabinet_info is None:
            return None

        cabinet_object: hard_mod.InstalledCabinet = hard_mod.InstalledCabinet(cabinet_info)

        return cabinet_object


    def install_new_shelf(self,header:dict,payload:dict) -> bool:
        cabinet_object: hard_mod.InstalledCabinet | None = self.get_cabinet_info(header,payload)

        if cabinet_object is None:
            return False

        if cabinet_object.current_installed_shelf + 1 > cabinet_object.shelf_capacity:
            print(f"[HARDWAR - SERVICES] ARMÁRIO {cabinet_object.id} ATINGIU A CAPACIDADE MÁXIMA {cabinet_object.current_installed_shelf}\n")
            return False
        
        new_shelf_object: hard_mod.NewShelf = hard_mod.NewShelf(payload)

        attributes_fields = ["installed_cabinet_id","hardware_mac_address", "hardware_tcp_port"]

        new_shelf_dict = self.attributes_to_dict(new_shelf_object, attributes_fields)

        result = hard_dao.add_new_shelf(new_shelf_dict,cabinet_object.id)

        return result


    def get_shelf_info(self,header:dict,payload:dict) -> hard_mod.InstalledShelf | None:
        shelf_info: dict = hard_dao.get_shelf_info(payload["shelf_id"])

        if shelf_info is None:
            return None

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

# def test_new_cabinet():
#     sample_payload = {
#         "header":
#         {
#             "correlation_id": "req_8f3a9b1c-2026",
#             "client_type": "totem",
#             "client_id": "TOTEM_LOJA_01",
#             "user_id": "3",
#             "role": "employee", #consumer, employee, manager
#             "auth_token": "bearer.jwt.token.here",
#             "action": "INSTALL_NEW_CABINET", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO
#             "timestamp": "1785816136"
#         },
#         "payload":
#         {
#             "hardware_mac_address": "16:58:PL:18:JI:67",
#             "hardware_tcp_port": "80001",
#             "hardware_current_ip_address": "192.168.1.243"
#         },
#     }

#     hardware_obj = HardwareServices()

#     result = hardware_obj.process_payload(sample_payload)

#     assert result == True

# def test_new_shelfs():
#     sample_payload = {
#         "header": { 
#             "correlation_id": "req_8f3a9b1c-2026",
#             "client_type": "totem",
#             "client_id": "TOTEM_LOJA_01",
#             "user_id": "3",
#             "role": "employee", #consumer, employee, manager
#             "auth_token": "bearer.jwt.token.here",
#             "action": "INSTALL_NEW_SHELF", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO, LIST_ALL_CABINETS, LIST_ALL_SHELFS
#             "timestamp": "1785816136"
#         },
#         "payload": {
#             "installed_cabinet_id": 3,
#             "hardware_mac_address": "16:58:PL:18:JI:53",
#             "hardware_tcp_port": "80002",
#             "hardware_current_ip_address": "192.168.1.263"

#         }
#     }

#     hardware_obj = HardwareServices()

#     mac_address_list = [
#     "00:1A:2B:3C:4D:01",
#     "00:1A:2B:3C:4D:02",
#     "00:1A:2B:3C:4D:03",
#     "00:1A:2B:3C:4D:04",
#     "00:1A:2B:3C:4D:05",
#     "00:1A:2B:3C:4D:06",
#     "00:1A:2B:3C:4D:07",
#     "00:1A:2B:3C:4D:08",
#     "00:1A:2B:3C:4D:09",
#     "00:1A:2B:3C:4D:0A",
#     "00:1A:2B:3C:4D:0B",
#     "00:1A:2B:3C:4D:0C",
#     "00:1A:2B:3C:4D:0D",
#     "00:1A:2B:3C:4D:0E",
#     "00:1A:2B:3C:4D:0F"
#     ]

#     # Lista com 15 endereços IP únicos para teste (na mesma sub-rede)
#     ip_list = [
#         "192.168.1.10",
#         "192.168.1.11",
#         "192.168.1.12",
#         "192.168.1.13",
#         "192.168.1.14",
#         "192.168.1.15",
#         "192.168.1.16",
#         "192.168.1.17",
#         "192.168.1.18",
#         "192.168.1.19",
#         "192.168.1.20",
#         "192.168.1.21",
#         "192.168.1.22",
#         "192.168.1.23",
#         "192.168.1.24"
#     ]
#     i = 0
#     for shelf in range(5):

#         sample_payload["payload"]["installed_cabinet_id"] = 1
#         sample_payload["payload"]["hardware_mac_address"] = mac_address_list[i]
#         sample_payload["payload"]["hardware_current_ip_address"] = ip_list[i]
#         result = hardware_obj.process_payload(sample_payload)
#         print (result)

        
#         sample_payload["payload"]["installed_cabinet_id"] = 2
#         sample_payload["payload"]["hardware_mac_address"] = mac_address_list[i+5]
#         sample_payload["payload"]["hardware_current_ip_address"] = ip_list[i+5]
#         hardware_obj.process_payload(sample_payload)
#         result = hardware_obj.process_payload(sample_payload)
#         print (result)
        
#         sample_payload["payload"]["installed_cabinet_id"] = 3
#         sample_payload["payload"]["hardware_mac_address"] = mac_address_list[i+10]
#         sample_payload["payload"]["hardware_current_ip_address"] = ip_list[i+10]
#         hardware_obj.process_payload(sample_payload)
#         result = hardware_obj.process_payload(sample_payload)
#         print (result)
#         i += 1
#     pass