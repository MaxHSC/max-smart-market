def new_product_validation(price: float, product_weight: float, product_volume: int) -> bool:
    try:
        if price < 0:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: VALOR [{price}]\n")
            return False
        
        if product_weight <= 0:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: PESO [{product_weight}]\n")
            return False
        
        if product_volume < 0:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: QUANTIDADE [{product_volume}]\n")
            return False

        return True

    except ValueError:
            return False

def change_product_info_validation(selected_column:str, new_value: any) -> bool:
    try:
        allowed_key_names = [
                "product_name",
                "price",
                "product_volume",
                "available"
            ]
        
        if selected_column not in allowed_key_names:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: [{selected_column}]\n")
            raise ValueError("\n[BANCO DE DADOS - INVENTÁRIO] INFORMAÇÃO DE PRODUTO INVÁLIDA.")
        
        if selected_column == "price" and new_value < 0.0:
            raise ValueError("\n[BANCO DE DADOS - INVENTÁRIO] PREÇO INVÁLIDO.")
        if selected_column == "product_volume" and new_value < 0:
            raise ValueError("\n[BANCO DE DADOS - INVENTÁRIO] QUANTIDADE INVÁLIDA.")
        if selected_column == "available" and not isinstance(new_value, bool):
            raise ValueError("\n[BANCO DE DADOS - INVENTÁRIO] INFORMAÇÃO DE DISPONIBILIDADE INVÁLIDA.")

        return True

    except ValueError:
        return False

def reserve_oder_validation(order: list) -> bool: #VARIÁVEIS SERÃO DEFINIDAS À MEDIDA QUE O CÓDIGO FOR EVOLUINDO, POR HORA A ESTRUTURA SERÁ ESSA. DTO OU EXTRAÇÃO DIRETA NO DICT
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


payload_sample ={
  "header": {
    "correlation_id": "req_8f3a9b1c-2026",
    "client_type": "totem",
    "client_id": "TOTEM_LOJA_01",
    "role": "consumer",
    "auth_token": "bearer.jwt.token.here",
    "action": "ORDER_CREATE",
    "timestamp": 1785816136
  },
  "payload": {
    "items": [
      { "product_id": 104, "quantity": 2 }
    ],
    "payment_method": "PIX"
  }
}