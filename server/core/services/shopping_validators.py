#region VALIDATE GENERAL STRUCTURE
def structure_validation(payload: dict) -> bool:
    header_keys = [
        "correlation_id",
        "client_type",
        "client_id",
        "role",
        "auth_token",
        "action",
        "timestamp"
    ]

    try:
        if not isinstance(payload, dict): # 1 - VERIFICA SE O PAYLOAD É UM DICIONÁRIO
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        if "header" not in payload or "payload" not in payload: # 2 - VERIFICA SE O PAYLOAD POSSUI AS CHAVES "header" E "payload"
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        if not isinstance(payload["header"], dict) or not isinstance(payload["payload"], dict): # 3 - VERIFICA SE AS CHAVES "header" E "payload" SÃO DICIONÁRIOS
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        if not all(key in payload["header"] for key in header_keys): # 4 - VERIFICA SE O DICIONÁRIO "header" POSSUI TODAS AS CHAVES NECESSÁRIAS
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        for key in payload["header"]: # 4 - VERIFICA SE O DICIONÁRIO "header" POSSUI AS CHAVES CORRETAS
            if key not in header_keys:
                raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

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
                "role": "employee",
                "auth_token": "bearer.jwt.token.here",
                "action": "CHANGE_PRODUCT_INFO",
                "timestamp": "1785816136"
            },
            "payload": {
                "items": {
                    "product_id": 99, #int
                    "column_to_change": "price", #product_name, price, product_volume, available
                    "new_value": 10.99 #str, int/float, float, bool
                }
            }
        }
    column_keys = ["product_name", "price", "product_volume", "available"]
    try:
        if "items" not in payload["payload"] or not isinstance(payload["payload"]["items"], dict) or len(payload["payload"]["items"]) == 0: # 1 - VERIFICA SE O PAYLOAD POSSUI A CHAVE "items" E SE É UMA DICT NÃO VAZIO
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        items = payload["payload"]["items"]

        if "column_to_change" not in items or "new_value" not in items or "product_id" not in items: # 2 - VERIFICA SE O DICT items POSSUI AS CHAVES column_to_change, new_value E product_id
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        if not isinstance(items["product_id"], int): # 3 - VERIFICA SE O TIPO DE DADOS EM product_id É UM INT
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        if items["column_to_change"] not in column_keys: # 4 - VERIFICA SE OS VALORES DA CHAVE column_to_change SÃO PERMITIDOS
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        # 5 - CHECAGEM DE DADOS PARA CADA TIPO DE COLUNA (VALOR EM column_to_change)
        column_to_change = payload["payload"]["items"]["column_to_change"]
        new_value = payload["payload"]["items"]["new_value"]

        if column_to_change == "product_name" and (not isinstance(new_value, str) or not new_value.strip()): # 4 - VERIFICA SE O TIPO DE DADOS EM product_name É STRING
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        if column_to_change == "price" and (not isinstance(new_value, (int, float)) or new_value < 0): # 5 - VERIFICA SE O TIPO DE DADOS EM price É INT/FLOAT E SE O VALOR NÃO É MENOR QUE 0
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        if column_to_change == "product_volume" and (not isinstance(new_value, (int, float)) or new_value < 0):# 6 - VERIFICA SE O TIPO DE DADOS EM product_volume É INT/FLOAT E SE O VALOR NÃO É MENOR QUE 0
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        if column_to_change == "available" and not isinstance(new_value, bool): # 7 - VERIFICA SE O TIPO DE DADOS EM available É BOOL.
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
            
        return True
    
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion

#region VALIDATE NEW PROD
def new_product_validation(payload: dict) -> bool:
    sample_payload = {
        "header": { 
            "correlation_id": "req_8f3a9b1c-2026",
            "client_type": "totem",
            "client_id": "TOTEM_LOJA_01",
            "role": "employee",
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
        if "items" not in payload["payload"] or not isinstance(payload["payload"]["items"], dict) or len(payload["payload"]["items"]) == 0: # 1 - VERIFICA SE O PAYLOAD POSSUI A CHAVE "items" E SE É UM DICT NÃO VAZIO
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        item = payload["payload"]["items"]
        
        if not all(key in item for key in product_keys): # 2 - VERIFICA SE O DICT items POSSUI TODAS AS CHAVES NECESSÁRIAS
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        if not all(key in product_keys for key in item): # 3 - VERIFICA SE O DICT items POSSUI CHAVES CORRETAS
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        if not isinstance(item["price"], (int, float)) or item["price"] < 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        if not isinstance(item["product_weight"], (int, float)) or item["product_weight"] <= 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")
        
        if  not isinstance(item["product_volume"], (int, float)) or item["product_volume"] < 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        if not isinstance(item["cabinet_shelf_id"], int) or item["cabinet_shelf_id"] <= 0:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        if not isinstance(item["validity"], str) or not isinstance(item["product_batch"], str) or not isinstance(item["product_name"], str):
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        if not item["product_name"].strip() or not item["product_batch"].strip() or item["validity"].strip():
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA")

        return True

    except ValueError as e:
        print(f"\n[BANCO DE DADOS - PRODUTOS] ESTRUTURA DE DADOS INVÁLIDA: [{e}]") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. LEMBRAR DE REMOVER A INDICAÇÃO DO ERRO.
        return False
#endregion

#region VALIDATE RESERVE
def reserve_oder_validation(payload: dict) -> bool: #VARIÁVEIS SERÃO DEFINIDAS À MEDIDA QUE O CÓDIGO FOR EVOLUINDO, POR HORA A ESTRUTURA SERÁ ESSA. DTO OU EXTRAÇÃO DIRETA NO DICT
    
    try:
        if not isinstance(order, list):
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: TIPO DE DADOS NÃO PERMITIDO.")
        if len(order) == 0:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: LISTA VAZIA.")
        if client_type not in ["totem", "app"]:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: TIPO DE CLIENTE NÃO PERMITIDO.")
        if not client_id:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: ID DE CLIENTE NÃO INFORMADO.")
        if role not in ["consumer"]:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: TIPO DE CLIENTE NÃO PERMITIDO.")
        if not auth_token:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: TOKEN DE AUTENTICAÇÃO NÃO INFORMADO.")

        if not isinstance(order, list):
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: TIPO DE DADOS NÃO PERMITIDO.")
        for item in order:
            if not isinstance(item, dict):
                raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: TIPO DE DADOS NÃO PERMITIDO.")
            if "product_id" not in item or "quantity" not in item:
                raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: INFORMAÇÕES DO PRODUTO INVÁLIDAS.")
            if not isinstance(item["product_id"], int) or not isinstance(item["quantity"], int):
                raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: INFORMAÇÕES DO PRODUTO INVÁLIDAS.")
            if item["quantity"] <= 0:
                raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: QUANTIDADE DEVE SER MAIOR QUE ZERO.")

        if payment_method not in ["PIX", "CREDIT_CARD", "DEBIT_CARD"]:
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: MÉTODO DE PAGAMENTO NÃO PERMITIDO.")

        return True
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - COMPRAS] PEDIDO INVÁLIDO: {e}") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. DEPOIS REMOVER.
        return False

def confirm_payment_validation(order_number: int, total_order_price: float, inserted_value: float) -> bool:
    try:
        if not isinstance(order_number, int):
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] CONFIRMAÇÃO DE PAGAMENTO INVÁLIDA: NÚMERO DO PEDIDO INVÁLIDO.")
        if not isinstance(total_order_price, (int, float)):
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] CONFIRMAÇÃO DE PAGAMENTO INVÁLIDA: VALOR TOTAL DO PEDIDO INVÁLIDO.")
        if not isinstance(inserted_value, (int, float)):
            raise ValueError("\n[BANCO DE DADOS - COMPRAS] CONFIRMAÇÃO DE PAGAMENTO INVÁLIDA: VALOR INSERIDO INVÁLIDO.")

        return True
    except ValueError as e:
        print(f"\n[BANCO DE DADOS - COMPRAS] CONFIRMAÇÃO DE PAGAMENTO INVÁLIDA: {e}") #MANTER APENAS ENQUANTO O CÓDIGO ESTIVER EM DESENVOLVIMENTO, PARA DEBUG. DEPOIS REMOVER.
        return False


#region ACTION TARGET
def action_target(payload: dict):
    action_mapping = {
        "NEW_PRODUCT": new_product_validation,
        "CHANGE_PRODUCT_INFO": change_product_info_validation,
        "ORDER_CREATE": reserve_oder_validation,
        "ORDER_CANCEL": reserve_oder_validation,
        "ORDER_RESTORE": reserve_oder_validation,
        "SUSPEND_PRODUCT": suspend_product_validation,
        "UNSUSPEND_PRODUCT": unsuspend_product_validation,
        "GET_PRODUCTS_LIST": get_products_list_validation,
        "GET_PRODUCT_INFO": get_product_info_validation,
    }
    try:
        action = payload.get("header", {}).get("action")

        if action not in action_mapping:
            raise ValueError("\n[BANCO DE DADOS - PRODUTOS] AÇÃO INVÁLIDA")

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

payload_sample ={
  "header": {
    "correlation_id": "req_8f3a9b1c-2026",
    "client_type": "totem",
    "client_id": "TOTEM_LOJA_01",
    "role": "consumer",
    "auth_token": "bearer.jwt.token.here",
    "action": "ORDER_CREATE",
    "timestamp": "1785816136"
  },
  "payload": {
    "items": [
      { "product_id": 104, "quantity": 2, "*selected_column": "product_name", "*new_value": "New Product Name" }
    ],
    "payment_method": ["PIX", "CREDIT_CARD", "DEBIT_CARD", "MAINTENANCE"]
  }
}