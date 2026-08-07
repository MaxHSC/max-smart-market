#COMEÇAR CÓDIGO PARA MANUSEIO DOS DISPOSITIVOS DE HARDWARE, COMO ARMÁRIOS E PRATELEIRAS, QUE SERÃO UTILIZADOS PARA O FUNCIONAMENTO DO SISTEMA DE SUPERMERCADO INTELIGENTE.
from server.database import hardware_dao as hard_dao



def add_new_cabinet(cabinet_info: dict) -> bool:
    result = hard_dao.add_new_cabinet(cabinet_info)

    return result

def add_new_shelf(shelf_info: dict, cabinet_id: int) -> bool:
    result = hard_dao.add_new_shelf(shelf_info,cabinet_id)

    return result

def list_all_cabinets() -> list[dict]:
    cabinet_list = hard_dao.list_all_cabinets()

    return cabinet_list

def list_all_installed_shelf() -> list[dict]:
    isntalled_shelf_list = hard_dao.list_all_installed_shelf()

    return installed_shelf_list

def search_shelf_id(shelf_id: int) -> dict:
    shelf_info = hard_dao.search_shelf_id(shelf_id)

    return shelf_info

def remove_shelf(shelf_id: int) -> bool:
    shelf_info = search_shelf_id(shelf_id)

    installed_cabinet_id = shelf_info["installed_cabinet_id"]
    