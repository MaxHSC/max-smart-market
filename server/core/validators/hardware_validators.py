#region VALIDATE GENERAL STRUCTURE
def structure_validation(payload: dict) -> bool:
    sample_payload = {
        "header": { 
            "correlation_id": "req_8f3a9b1c-2026",
            "client_type": "totem",
            "client_id": "TOTEM_LOJA_01",
            "user_id": "3",
            "role": "employee", #consumer, employee, manager
            "auth_token": "bearer.jwt.token.here",
            "action": "INSTALL_NEW_CABINET", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO, LIST_ALL_CABINETS, LIST_ALL_SHELFS
            "timestamp": "1785816136"
        },
        "payload": {
            "hardware_mac_address": "xx:xx:xx:xx:xx",
            "hardware_tcp_port": "80001",
            "hardware_current_ip_address": "192.168.1.245"
        }
    }
    header_keys = [
        "correlation_id",
        "client_type",
        "client_id",
        "user_id",
        "role",
        "auth_token",
        "action",
        "timestamp"
    ]

    try:
        #[1] - VERIFICA SE O PAYLOAD BRUTO É UM DICIONÁRIO
        if not isinstance(payload, dict):
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[2] - VERIFICA SE O PAYLOAD BRUTO POSSUI AS CHAVES "header" E "payload"
        if "header" not in payload or "payload" not in payload:
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[3] - VERIFICA SE AS CHAVES "header" E "payload" SÃO DICIONÁRIOS
        if not isinstance(payload["header"], dict) or not isinstance(payload["payload"], dict):
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")

        #[4] - VERIFICA SE O DICIONÁRIO "header" POSSUI TODAS AS CHAVES NECESSÁRIAS E QUE TODAS SÃO CORRETAS, SEM EXTRAS
        if set(payload["header"]) != set(header_keys):
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")

        #[5] - VERIFICA SE OS VALORES DAS CHAVES DE header SÃO STR E SE NÃO SÃO TEXTOS VAZIOS
        for value in payload["header"].values():
            if not isinstance(value, str) or not value.strip():
                raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")

        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion

#region VALIDATE NEW CABINET
def install_new_cabinet_validation(payload: dict) -> bool:
    sample_payload = {
        "header": { 
            "correlation_id": "req_8f3a9b1c-2026",
            "client_type": "totem",
            "client_id": "TOTEM_LOJA_01",
            "user_id": "3",
            "role": "employee", #consumer, employee, manager
            "auth_token": "bearer.jwt.token.here",
            "action": "INSTALL_NEW_CABINET", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO, LIST_ALL_CABINETS, LIST_ALL_SHELFS
            "timestamp": "1785816136"
        },
        "payload": {
            "hardware_mac_address": "xx:xx:xx:xx:xx",
            "hardware_tcp_port": "80001",
            "hardware_current_ip_address": "192.168.1.245"
        }
    }

    payload_keys = ["hardware_mac_address", "hardware_tcp_port", "hardware_current_ip_address"]

    try:
        #[1] - VERIFICA SE O DICT payload POSSUI TODAS AS CHAVES NECESSÁRIAS E QUE TODAS SÃO CORRETAS, SEM CHAVES EXTRA
        if set(payload["payload"]) != set(payload_keys):
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[2] - VERIFICA SE TODOS OS VALORES EM payload SÃO DO TIPO STR E SE NÃO ESTÃO VAZIOS.
        for value in payload["payload"].value():
            if not isinstance(value, str) or not value.strip():
                raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion

#region VALIDATE GET CABINET
def get_cabinet_info_validation(payload: dict) -> bool:
    sample_payload = {
        "header": { 
            "correlation_id": "req_8f3a9b1c-2026",
            "client_type": "totem",
            "client_id": "TOTEM_LOJA_01",
            "user_id": "3",
            "role": "employee", #consumer, employee, manager
            "auth_token": "bearer.jwt.token.here",
            "action": "GET_CABINET_INFO", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO, LIST_ALL_CABINETS, LIST_ALL_SHELFS
            "timestamp": "1785816136"
        },
        "payload": {
            "installed_cabinet_id": 8
        }
    }

    try:
        #[1] - VERIFICA SE A CHAVE installed_cabinet_id EXISTE NO DICT payload E SE NÃO EXISTE MAIS DE UMA CHAVE
        if "installed_cabinet_id" not in payload["payload"] or len(payload["payload"]) != 1:
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[2] - VERIFICA SE O VALOR DE installed_cabinet_id É UM INT E SE É MAIOR QUE ZERO.
        if not isinstance(payload["payload"]["installed_cabinet_id"], int) or len(payload["payload"]["installed_cabinet_id"]) <= 0:
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion


#region VALIDATE NEW SHELF
def install_new_shelf_validation(payload: dict) -> bool:
    sample_payload = {
        "header": { 
            "correlation_id": "req_8f3a9b1c-2026",
            "client_type": "totem",
            "client_id": "TOTEM_LOJA_01",
            "user_id": "3",
            "role": "employee", #consumer, employee, manager
            "auth_token": "bearer.jwt.token.here",
            "action": "INSTALL_NEW_SHELF", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO, LIST_ALL_CABINETS, LIST_ALL_SHELFS
            "timestamp": "1785816136"
        },
        "payload": {
            "installed_cabinet_id": "8",
            "hardware_mac_address": "xx:xx:xx:xx:xx",
            "hardware_tcp_port": "80001",
            "hardware_current_ip_address": "192.168.1.245"

        }
    }
    payload_keys = ["installed_cabinet_id","hardware_mac_address", "hardware_tcp_port", "hardware_current_ip_address"]

    try:
        #[1] - VERIFICA SE O DICT payload POSSUI TODAS AS CHAVES NECESSÁRIAS E QUE TODAS SÃO CORRETAS, SEM CHAVES EXTRA
        if set(payload["payload"]) != set(payload_keys):
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[2] - VERIFICA SE TODOS OS VALORES EM payload SÃO DO TIPO STR E SE NÃO ESTÃO VAZIOS.
        for value in payload["payload"]:
            if not isinstance(value, str) or not value.strip():
                raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion


#region VALIDATE GET SHELF
def get_shelf_info_validation(payload: dict) -> bool:
    sample_payload = {
        "header": { 
            "correlation_id": "req_8f3a9b1c-2026",
            "client_type": "totem",
            "client_id": "TOTEM_LOJA_01",
            "user_id": "3",
            "role": "employee", #consumer, employee, manager
            "auth_token": "bearer.jwt.token.here",
            "action": "GET_SHELF_INFO", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO, LIST_ALL_CABINETS, LIST_ALL_SHELFS
            "timestamp": "1785816136"
        },
        "payload": {
            "shelf_id": 8
        }
    }

    try:
        #[1] - VERIFICA SE A CHAVE shelf_id EXISTE NO DICT payload E SE NÃO EXISTE MAIS DE UMA CHAVE
        if "shelf_id" not in payload["payload"] or len(payload["payload"]) != 1:
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[2] - VERIFICA SE O VALOR DE shelf_id É UM INT E SE É MAIOR QUE ZERO.
        if not isinstance(payload["payload"]["shelf_id"], int) or len(payload["payload"]["shelf_id"]) <= 0:
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA.")
        
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - HARDWARES] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion


#region NO VALIDATIONS
#DEFS NULAS, EXISTEM APENAS PARA GARANTIR O MAPPING DE action_target
def list_all_cabinets_validation(payload: dict) -> bool:
    return True

def list_all_shelfs_validation(payload: dict) -> bool:
    return True
#endregion

#region ACTION TARGET
def action_target(payload: dict):
    action_mapping = {
        "INSTALL_NEW_CABINET": install_new_cabinet_validation,
        "GET_CABINET_INFO": get_cabinet_info_validation,
        "INSTALL_NEW_SHELF": install_new_shelf_validation,
        "GET_SHELF_INFO": get_shelf_info_validation,
        "LIST_ALL_CABINETS": list_all_cabinets_validation,
        "LIST_ALL_SHELFS": list_all_shelfs_validation,
    }
    try:
        action = payload.get("header", {}).get("action")
        
        if action not in action_mapping:
            raise ValueError("\n[BANCO DE DADOS - HARDWARES] AÇÃO INVÁLIDA.")

        return action_mapping[action]

    except ValueError as e:
        print(f"\n[BANCO DE DADOS - HARDWARES] AÇÃO INVÁLIDA: [{e}]")
        return False


def payload_validation(payload: dict) -> bool:
    general_structure_result = structure_validation(payload)

    if not general_structure_result:
        return False
    
    type_action_result = action_target(payload)

    if not type_action_result:
        return False

    action_result = type_action_result(payload)

    if not action_result:
        return False

    return True
#endregion