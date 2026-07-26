from server.database import inventory_dao as inv


def new_product(bar_code: int, product_name: str, price: float, product_batch: str, validity: str, weight_gram_unit: float, cabinet_shelf_id: int, total_inventory_amount: int) -> bool:
    try:
        if price < 0:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: VALOR [{price}]\n")
            return False
        
        if weight_gram_unit <= 0:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: PESO [{weight_gram_unit}]\n")
            return False
        
        if total_inventory_amount < 0:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: QUANTIDADE [{total_inventory_amount}]\n")
            return False

        inv.add_new_product(bar_code, product_name, price, product_batch, validity, weight_gram_unit, cabinet_shelf_id, total_inventory_amount)

    except ValueError:
        return False

    return True


def change_product_info(product_id,selected_column,new_value) -> bool:
    try:
        allowed_key_names = [
                "product_name",
                "bar_code",
                "price",
                "product_batch",
                "validity",
                "weight_gram_unit",
                "cabinet_shelf_id",
                "total_inventory_amount",
                "avaliable"
            ]
        
        if selected_column not in allowed_key_names:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: [{selected_column}]\n")
            return False
        
        if selected_column == "price" and new_value < 0:
            raise ValueError("\n[BANCO DE DADOS - INVENTÁRIO] PREÇO INVÁLIDO.")

        inv.change_product_info(product_id,selected_column,new_value)

    except ValueError:
        return False
    
    return True

def search_product_name(product_name) -> list:
    return inv.search_product_name(product_name)

def list_all_products() -> list:
    return inv.list_all_products()

def checkou_cart(cart: list) -> bool:
    return inv.checkout_cart(cart)










#region TEST AREA

# def test_cart_checkout():
#     cart_list = [{"id":7,"amount":1},{"id":5,"amount":1},{"id":1,"amount":4},{"id":4,"amount":3}]

#     checkou_cart(cart_list)




# def test_new_product():
#     prod = [
#         12368974,
#         "PIZZA CONGELADA SADIA MUSSARELA",
#         16.00,
#         "SDAMCZ260726PZML",
#         "2028-07-26",
#         460.0,
#         15,
#         4
#     ]

#     bar_code = prod[0]
#     product_name = prod[1]
#     price = prod[2]
#     product_batch = prod[3]
#     validity = prod[4]
#     weight_gram_unit = prod[5]
#     cabinet_shelf_id = prod[6]
#     total_inventory_amount = prod[7]

#     new_product(bar_code, product_name, price, product_batch, validity, weight_gram_unit, cabinet_shelf_id, total_inventory_amount)
#     pass

# def test_list_prod():
#     prod_list = list_all_products()

#     for prod in prod_list:
#         print("\n--------[INFORMAÇÕES DO PRODUTO]-------")
#         print(f"[PRODUTO] {prod["product_name"]}")
#         print(f"[PREÇO] R${prod["price"]}")
#         print(f"[VALIDADE] {prod["validity"]}")
#         print(f"[PESO EM GRAMAS] {prod["weight_gram_unit"]}g")
#         print(f"[ID] {prod["id"]}")
#         print(f"[CÓDIGO DE BARRAS] {prod["bar_code"]}")
#         print(f"[PRATELEIRA] N#{prod["cabinet_shelf_id"]}")
#         print(f"[QUANTIDADE DISPONÍVEL] {prod["total_inventory_amount"]}")
#         print("\n\n")

# def test_change_prod_info():
#     product_id = 2
#     selected_column = "total_inventory_amount"
#     new_value = 10

#     change_product_info(product_id,selected_column,new_value)

#     prod_list = search_product_name("350")

#     for prod in prod_list:
#         print("\n--------[INFORMAÇÕES DO PRODUTO]-------")
#         print(f"[PRODUTO] {prod["product_name"]}")
#         print(f"[PREÇO] R${prod["price"]}")
#         print(f"[VALIDADE] {prod["validity"]}")
#         print(f"[PESO EM GRAMAS] {prod["weight_gram_unit"]}g")
#         print(f"[ID] {prod["id"]}")
#         print(f"[CÓDIGO DE BARRAS] {prod["bar_code"]}")
#         print(f"[PRATELEIRA] N#{prod["cabinet_shelf_id"]}")
#         print(f"[QUANTIDADE DISPONÍVEL] {prod["total_inventory_amount"]}")
#         print("\n\n")

#     pass

#endregion