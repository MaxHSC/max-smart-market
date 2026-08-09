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
            "action": "CHANGE_PRODUCT_INFO",
            "timestamp": "1785816136"
        },
        "payload": {
            "item": {
                "product_id": 99, #int
                "column_to_change": "price", #product_name, price, product_volume, available
                "new_value": 10.99 #str, int/float, float, bool
            }
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
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[2] - VERIFICA SE O PAYLOAD BRUTO POSSUI AS CHAVES "header" E "payload"
        if "header" not in payload or "payload" not in payload:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[3] - VERIFICA SE AS CHAVES "header" E "payload" SÃO DICIONÁRIOS
        if not isinstance(payload["header"], dict) or not isinstance(payload["payload"], dict):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[4] - VERIFICA SE O DICIONÁRIO "header" POSSUI TODAS AS CHAVES NECESSÁRIAS E QUE TODAS SÃO CORRETAS, SEM EXTRAS
        if set(payload["header"]) != set(header_keys):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[5] - VERIFICA SE OS VALORES DAS CHAVES DE header SÃO STR E SE NÃO SÃO TEXTOS VAZIOS
        for value in payload["header"].values():
            if not isinstance(value, str) or not value.strip() <= 0:
                raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion


#region VALIDATE CHANGES
def change_product_info_validation(payload: dict) -> bool:
    sample_payload = {
            "header": { 
                "correlation_id": "req_8f3a9b1c-2026",
                "client_type": "totem",
                "client_id": "TOTEM_LOJA_01",
                "user_id": "3",
                "role": "employee", #consumer, employee, manager
                "auth_token": "bearer.jwt.token.here",
                "action": "CHANGE_PRODUCT_INFO",
                "timestamp": "1785816136"
            },
            "payload": {
                "item": { #ITEM SEM S, NO SINGULAR
                    "product_id": 99, #int
                    "column_to_change": "price", #product_name, price, product_volume, available
                    "new_value": 10.99 #str, int/float, float, bool
                }
            }
        }
    column_keys = ["product_name", "price", "product_volume", "available"]
    item_keys = ["product_id", "column_to_change", "new_value"]

    try:
        #[1] - VERIFICA SE O PAYLOAD POSSUI A CHAVE "item" E SE É UM DICT NÃO VAZIO
        if "item" not in payload["payload"] or not isinstance(payload["payload"]["item"], dict) or len(payload["payload"]["item"]) == 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        item = payload["payload"]["item"]

        #[2] - VERIFICA SE O DICT item POSSUI AS CHAVES column_to_change, new_value E product_id
        if set(item) != set(item_keys):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[3] - VERIFICA SE O TIPO DE DADOS EM product_id É UM INT
        if not isinstance(item["product_id"], int):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[4] - VERIFICA SE OS VALORES DA CHAVE column_to_change SÃO PERMITIDOS
        if item["column_to_change"] not in column_keys:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[5] - CHECAGEM DE DADOS PARA CADA TIPO DE COLUNA (VALOR EM column_to_change)
        column_to_change = payload["payload"]["item"]["column_to_change"]
        new_value = payload["payload"]["item"]["new_value"]

        #[5.1] - VERIFICA SE O TIPO DE DADOS EM product_name É STRING
        if column_to_change == "product_name" and (not isinstance(new_value, str) or not new_value.strip()):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[5.2] - VERIFICA SE O TIPO DE DADOS EM price É INT/FLOAT E SE O VALOR NÃO É MENOR QUE 0
        if column_to_change == "price" and (not isinstance(new_value, (int, float)) or new_value < 0):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[5.3] - VERIFICA SE O TIPO DE DADOS EM product_volume É INT/FLOAT E SE O VALOR NÃO É MENOR QUE 0
        if column_to_change == "product_volume" and (not isinstance(new_value, (int, float)) or new_value < 0):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[5.4] - VERIFICA SE O TIPO DE DADOS EM available É BOOL.
        if column_to_change == "available" and not isinstance(new_value, bool):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
            
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion

#region VALIDATE NEW
def new_product_validation(payload: dict) -> bool:
    sample_payload = {
        "header": { 
            "correlation_id": "req_8f3a9b1c-2026",
            "client_type": "totem",
            "client_id": "TOTEM_LOJA_01",
            "user_id": "3",
            "role": "employee", #consumer, employee, manager
            "auth_token": "bearer.jwt.token.here",
            "action": "NEW_PRODUCT",
            "timestamp": "1785816136"
        },
        "payload": {
            "items": {
                "product_name": "New Product",
                "price": 10.99,
                "product_batch": "BATCH_001",
                "validity": "2023-12-31",
                "product_weight": 1.5,
                "cabinet_shelf_id": 1,
                "product_volume": 2.0
            }
        }
    }

    product_keys = ["product_name", "price", "product_batch", "validity", "product_weight", "cabinet_shelf_id", "product_volume"]

    try:
        #[1] - VERIFICA SE O PAYLOAD POSSUI A CHAVE "items" E SE É UM DICT NÃO VAZIO
        if "items" not in payload["payload"] or not isinstance(payload["payload"]["items"], dict) or len(payload["payload"]["items"]) == 0: 
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        item = payload["payload"]["items"]
        
        #[2] - VERIFICA SE O DICT items POSSUI TODAS AS CHAVES NECESSÁRIAS E QUE TODAS SÃO CORRETAS, SEM CHAVES EXTRA
        if set(item) != set(product_keys):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[3] - CHECAGEM DE DADOS PARA CADA CHAVE
        if not isinstance(item["price"], (int, float)) or item["price"] < 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[3.1] - VERIFICA SE O TIPO DE DADOS EM product_weight É FLOAT E SE É MAIOR QUE 0
        if not isinstance(item["product_weight"], (int, float)) or item["product_weight"] <= 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[3.2] - VERIFICA SE O TIPO DE DADOS EM product_volume É INT OU FLOAT E SE É MAIOR QUE 0
        if  not isinstance(item["product_volume"], (int, float)) or item["product_volume"] < 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[3.3] - VERIFICA SE O TIPO DE DADOS EM cabinet_shelf_id É INT E SE É MAIOR QUE 0
        if not isinstance(item["cabinet_shelf_id"], int) or item["cabinet_shelf_id"] <= 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[3.4] - VERIFICA SE O TIPO DE DADOS EM  validity, product_batch E product_name É STR
        if not isinstance(item["product_name"], str) or not isinstance(item["product_batch"], str) or not isinstance(item["validity"], str):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[3.5] - VERIFICA SE AS CHAVES product_name, product_batch E validity NÃO SÃO STRINGS VAZIAS
        if not item["product_name"].strip() or not item["product_batch"].strip() or item["validity"].strip():
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA.")

        return True

    except ValueError as e:
        print(f"\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion

#region VALIDATE RESERVE
def reserve_order_validation(payload: dict) -> bool: #VARIÁVEIS SERÃO DEFINIDAS À MEDIDA QUE O CÓDIGO FOR EVOLUINDO, POR HORA A ESTRUTURA SERÁ ESSA. DTO OU EXTRAÇÃO DIRETA NO DICT - EXTRAÇÃO DIRETA NO DICT
    sample_payload = {
            "header": { 
                "correlation_id": "req_8f3a9b1c-2026",
                "client_type": "totem",
                "client_id": "TOTEM_LOJA_01",
                "user_id": "3",
                "role": "employee", #consumer, employee, manager
                "auth_token": "bearer.jwt.token.here",
                "action": "ORDER_CREATE",
                "timestamp": "1785816136"
            },
            "payload": {
                "items": [ #ITEMS COM S, NO PLURAL, POIS É LISTA DE ITENS
                    {
                        "product_id": 29,
                        "quantity": 3,
                    }
                ],
            }
    }
    items_keys = ["product_id", "quantity"]
    try:
        #[1] - VERIFICA SE O PAYLOAD POSSUI A CHAVE items E SE É UMA LISTA NÃO VAZIA
        if "items" not in payload["payload"] or not isinstance(payload["payload"]["items"], list) or len(payload["payload"]["items"]) == 0:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        items = payload["payload"]["items"]

        #[2] - CHECAGEM DE DADOS PARA CADA ITEM EM items
        for item in items:
            #[2.1] - VERIFICA SE O ÍNDICE ATUAL EM items É UM DICT
            if not isinstance(item, dict):
                raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")

            #[2.2] - VERIFICA SE O DICIONÁRIO ATUAL EM items CONTÉM AS CHAVES NECESSÁRIAS E PERMITIDAS
            if set(item) != set(items_keys):
                raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")

            #[2.3] - VERIFICA SE product_id E quantity SÃO INT
            if not isinstance(item["product_id"], int) or not isinstance(item["quantity"], int):
                raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")

            #[2.4] - VERIFICA SE product_id E quantity SÃO MAIORES QUE 0
            if item["product_id"] <= 0 or item["quantity"] <= 0:
                raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")

        return True

    except ValueError as e:
        print(f"\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. DEPOIS REMOVER.
        return False
#endregion

#region VALIDATE RESTORE
def restore_order_validation(payload: dict) -> bool:
    sample_payload = {
                "header": { 
                    "correlation_id": "req_8f3a9b1c-2026",
                    "client_type": "totem",
                    "client_id": "TOTEM_LOJA_01",
                    "user_id": "3",
                    "role": "employee", #consumer, employee, manager
                    "auth_token": "bearer.jwt.token.here",
                    "action": "ORDER_RESTORE",
                    "timestamp": "1785816136"
                },
                "payload": {
                    "order_number": 564896,
                }
        }
    
    try:
        #[1] - VERIFICA SE A CHAVE order_number EXISTE NO DICT payload E SE NÃO EXISTE MAIS DE UMA CHAVE
        if "order_number" not in payload["payload"] or len(payload["payload"]) != 1:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[2] - VERIFICA SE O VALOR DE order_number É UM INT E SE É MAIOR QUE 0
        if not isinstance(payload["payload"]["order_number"], int) or payload["payload"]["order_number"] <= 0:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. DEPOIS REMOVER.
        return False
#endregion

#region VALIDATE CANCEL

def cancel_order_validation(payload: dict) -> bool:
    sample_payload = {
                "header": { 
                    "correlation_id": "req_8f3a9b1c-2026",
                    "client_type": "totem",
                    "client_id": "TOTEM_LOJA_01",
                    "user_id": "3",
                    "role": "employee", #consumer, employee, manager
                    "auth_token": "bearer.jwt.token.here",
                    "action": "ORDER_CANCEL",
                    "timestamp": "1785816136"
                },
                "payload": {
                    "order_number": 564896,
                }
        }
    
    try:
        #[1] - VERIFICA SE A CHAVE order_number EXISTE NO DICT payload E SE NÃO EXISTE MAIS DE UMA CHAVE
        if "order_number" not in payload["payload"] or len(payload["payload"]) != 1:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")

        #[2] - VERIFICA SE O VALOR DE order_number É UM INT E SE É MAIOR QUE 0
        if not isinstance(payload["payload"]["order_number"], int) or payload["payload"]["order_number"] <= 0:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. DEPOIS REMOVER.
        return False
#endregion

#region VALIDATE SUSPEND
def suspend_product_validation(payload: dict):
    sample_payload = {
                    "header": { 
                        "correlation_id": "req_8f3a9b1c-2026",
                        "client_type": "totem",
                        "client_id": "TOTEM_LOJA_01",
                        "user_id": "3",
                        "role": "employee", #consumer, employee, manager
                        "auth_token": "bearer.jwt.token.here",
                        "action": "SUSPEND_PRODUCT",
                        "timestamp": "1785816136"
                    },
                    "payload": {
                        "product_id": 29,
                    }
            }

    try:
        #[1] - VERIFICA SE A CHAVE product_id EXISTE NO DICT payload E SE NÃO EXISTE MAIS DE UMA CHAVE
        if "product_id" not in payload["payload"] or len(payload["payload"]) != 1:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[2] - VERIFICA SE O VALOR DE product_id É UM INT E SE É MAIOR QUE 0
        if not isinstance(payload["payload"]["product_id"], int) or payload["payload"]["product_id"] <= 0:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. DEPOIS REMOVER.
        return False
#endregion

#region VALIDATE UNSUSPEND
def unsuspend_product_validation(payload: dict):
    sample_payload = {
                    "header": { 
                        "correlation_id": "req_8f3a9b1c-2026",
                        "client_type": "totem",
                        "client_id": "TOTEM_LOJA_01",
                        "user_id": "3",
                        "role": "employee", #consumer, employee, manager
                        "auth_token": "bearer.jwt.token.here",
                        "action": "UNSUSPEND_PRODUCT",
                        "timestamp": "1785816136"
                    },
                    "payload": {
                        "product_id": 29,
                    }
            }

    try:
        #[1] - VERIFICA SE A CHAVE product_id EXISTE NO DICT payload E SE NÃO EXISTE MAIS DE UMA CHAVE
        if "product_id" not in payload["payload"] or len(payload["payload"]) != 1:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        #[2] - VERIFICA SE O VALOR DE product_id É UM INT E SE É MAIOR QUE 0
        if not isinstance(payload["payload"]["product_id"], int) or payload["payload"]["product_id"] <= 0:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA.")
        
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - COMPRAS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. DEPOIS REMOVER.
        return False
#endregion

#region NO VALIDATIONS
#DEFS NULAS, EXISTEM APENAS PARA GARANTIR O MAPPING DE action_target
def get_products_list_validation(payload: dict) -> bool:
    return True

def get_product_info_validation(payload: dict) -> bool:
    return True
#endregion

#region ACTION TARGET
def action_target(payload: dict):
    action_mapping = {
        "NEW_PRODUCT": new_product_validation,
        "CHANGE_PRODUCT_INFO": change_product_info_validation,
        "ORDER_CREATE": reserve_order_validation,
        "ORDER_CANCEL": cancel_order_validation,
        "ORDER_RESTORE": restore_order_validation,
        "SUSPEND_PRODUCT": suspend_product_validation,
        "UNSUSPEND_PRODUCT": unsuspend_product_validation,
        "GET_PRODUCTS_LIST": get_products_list_validation,
        "GET_PRODUCT_INFO": get_product_info_validation,
    }
    try:
        action = payload.get("header", {}).get("action")
        
        if action not in action_mapping:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] AÇÃO INVÁLIDA.")

        return action_mapping[action]

    except ValueError as e:
        print(f"\n[BANCO DE DADOS - PRODUTOS] AÇÃO INVÁLIDA: [{e}]")
        return False


def target_validation(payload: dict) -> bool:
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