from server.database import inventory_dao as inv
from server.core.models import products_models as prod_mod, payment_gateway_simulator as pay_gat


def new_product(bar_code: int, product_name: str, price: float, product_batch: str, validity: str, product_weight: float, cabinet_shelf_id: int, product_volume: int) -> bool:
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

        result = prod_mod.new_product(bar_code, product_name, price, product_batch, validity, product_weight, cabinet_shelf_id, product_volume)

        return result

    except ValueError:
        return False


def change_product_info(product_info,selected_column,new_value,command=None,product_weight=None) -> bool:
    try:
        allowed_key_names = [
                "product_name",
                "price",
                "product_volume",
                "avaliable"
            ]
        
        if selected_column not in allowed_key_names:
            print(f"\n[BANCO DE DADOS] INFORMAÇÃO DE PRODUTO INVÁLIDA: [{selected_column}]\n")
            return False
        
        if selected_column == "price" and new_value < 0:
            raise ValueError("\n[BANCO DE DADOS - INVENTÁRIO] PREÇO INVÁLIDO.")

        result = prod_mod.change_product_info(product_info,selected_column,new_value,command,product_weight)

    except ValueError:
        return False
    
    return result

def list_all_products() -> list:
    available_products_list = prod_mod.get_products_list()

    return available_products_list

def reserve_order(order: list) -> tuple:
    order_number, expires_time, user_id, total_order_price = prod_mod.reserve_order(order)

    return order_number, expires_time, user_id, total_order_price


def checkout_order(order: list) -> bool:
    result, new_shelfs_values_list, order_number, cabinet_id_list = prod_mod.checkout_cart(order)
    
    return result, new_shelfs_values_list, order_number, cabinet_id_list


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
#     product_weight = prod[5]
#     cabinet_shelf_id = prod[6]
#     product_volume = prod[7]

#     new_product(bar_code, product_name, price, product_batch, validity, product_weight, cabinet_shelf_id, product_volume)
#     pass

# def test_list_prod():
#     prod_list = list_all_products()

#     for prod in prod_list:
#         print("\n--------[INFORMAÇÕES DO PRODUTO]-------")
#         print(f"[PRODUTO] {prod["product_name"]}")
#         print(f"[PREÇO] R${prod["price"]}")
#         print(f"[VALIDADE] {prod["validity"]}")
#         print(f"[PESO EM GRAMAS] {prod["product_weight"]}g")
#         print(f"[ID] {prod["id"]}")
#         print(f"[CÓDIGO DE BARRAS] {prod["bar_code"]}")
#         print(f"[PRATELEIRA] N#{prod["cabinet_shelf_id"]}")
#         print(f"[QUANTIDADE DISPONÍVEL] {prod["product_volume"]}")
#         print("\n\n")

# def test_change_prod_info():
#     product_id = 2
#     selected_column = "product_volume"
#     new_value = 10

#     change_product_info(product_id,selected_column,new_value)

#     prod_list = search_product_name("350")

#     for prod in prod_list:
#         print("\n--------[INFORMAÇÕES DO PRODUTO]-------")
#         print(f"[PRODUTO] {prod["product_name"]}")
#         print(f"[PREÇO] R${prod["price"]}")
#         print(f"[VALIDADE] {prod["validity"]}")
#         print(f"[PESO EM GRAMAS] {prod["product_weight"]}g")
#         print(f"[ID] {prod["id"]}")
#         print(f"[CÓDIGO DE BARRAS] {prod["bar_code"]}")
#         print(f"[PRATELEIRA] N#{prod["cabinet_shelf_id"]}")
#         print(f"[QUANTIDADE DISPONÍVEL] {prod["product_volume"]}")
#         print("\n\n")

#     pass

#endregion