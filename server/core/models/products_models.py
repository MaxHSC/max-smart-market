from server.database import hardware_dao as hard_dao
from server.database import inventory_dao as inv_dao

#region PRODUCTS CHECK
def shelf_capacity_calculate(total_weight_cap,current_weight,delta_weight,total_volume_cap,current_volume,delta_volume,command) -> tuple:
    #CALCULATE SHELF CAPACITY WEIGHT AND VOLUME
    if command == "increase":
        new_weight = current_weight + (delta_weight*delta_volume)
        new_volume = current_volume + delta_volume

    elif command == "decrease":
        new_weight = current_weight - (delta_weight*delta_volume)
        new_volume = current_volume - delta_volume

    else:
        print(f"\n[BANCO DE DADOS - CHECAGEM DE PRATELEIRA] COMANDO INVÁLIDO. OPERAÇÃO CANCELADA\n")
        return False, None, None
    #END CHECK
    
    #CHECK NEW SHELF WEIGHT AND VOLUME 
    if new_weight > total_weight_cap or new_weight < 0:
        print(f"\n[BANCO DE DADOS CHECAGEM DE PRATELEIRA] ERRO NO CÁLCULO DE PESO. OPERAÇÃO CANCELADA\n")
        return False, None, None

    if new_volume > total_volume_cap or new_volume < 0:
        print(f"\n[BANCO DE DADOS CHECAGEM DE PRATELEIRA] ERRO NO CÁLCULO DE VOLUME. OPERAÇÃO CANCELADA\n")
        return False, None, None
    #END CHECK
    
    return True, new_weight, new_volume


def unpack_shelf_info(shelf_info: dict):
    shelf_weight_cap = shelf_info["weight_capacity_grams"]
    shelf_volume_cap = shelf_info["volume_capacity"]

    shelf_current_weight = shelf_info["current_weight_grams"] if shelf_info["current_weight_grams"] is not None else 0
    shelf_current_volume = shelf_info["current_volume"] if shelf_info["current_volume"] is not None else 0

    return shelf_weight_cap, shelf_volume_cap, shelf_current_weight, shelf_current_volume
#endregion


#region PRODUCTS ACTIONS
def new_product(bar_code: int, product_name: str, price: float, product_batch: str, validity: str, product_weight: float, cabinet_shelf_id: int, product_volume: int) -> bool:
    shelf_info = hard_dao.search_shelf_id(cabinet_shelf_id)

    if not shelf_info:
        return False

    shelf_weight_cap, shelf_volume_cap, shelf_current_weight, shelf_current_volume = unpack_shelf_info(shelf_info)

    new_cap_valid, shelf_new_weight, shelf_new_volume = shelf_capacity_calculate(shelf_weight_cap,shelf_current_weight,product_weight,shelf_volume_cap,shelf_current_volume,product_volume,"increase")

    if not new_cap_valid:
        return False

    result = inv_dao.add_new_product(bar_code, product_name, price, product_batch, validity, product_weight, cabinet_shelf_id, product_volume, shelf_new_weight, shelf_new_volume)

    return result


def change_product_info(product_info,selected_column,new_value,command=None):
    shelf_id = product_info["cabinet_shelf_id"]
    product_id = product_info["id"]

    if command:
        shelf_info = hard_dao.search_shelf_id(shelf_id)
        product_weight = product_info["product_weight"]
        product_delta_volume = product_info["product_volume"]

        if not shelf_info:
            return False

        shelf_weight_cap, shelf_volume_cap, shelf_current_weight, shelf_current_volume = unpack_shelf_info(shelf_info)
    
        new_cap_valid, shelf_new_weight, shelf_new_volume = shelf_capacity_calculate(shelf_weight_cap,shelf_current_weight,product_weight,shelf_volume_cap,shelf_current_volume,product_delta_volume,command)

        if not new_cap_valid:
            return False
        
        result = inv_dao.change_product_info(product_id,selected_column,new_value,command,shelf_id,shelf_new_weight,shelf_new_volume)


def checkout_cart(cart: list):
    '''cart ALWAYS MUST TO BE RECEIVED AS A LIST OF DICT WITH ID AND VOLUME TO BE BOUGHT
    [
        {
            "id":19,
            "product_volume":3
        },
    ]
    AND SEND WITH NEW STOCK VALUES AND CART DICT
    [
        {"id":19,
        "new_product_volume":3,
        "cabinet_shelf_id":5,
        "new_shelf_weight":15.0,
        "new_shelf_volume":15
        },
    ]
    '''
    final_cart = []

    for prod in cart:
        product_current_volume, product_weight, shelf_id = inv_dao.get_product_info(prod["id"])
        
        if not product_current_volume:
            return False

        product_volume = prod["product_volume"]
        shelf_info = hard_dao.search_shelf_id(shelf_id)

        shelf_weight_cap, shelf_volume_cap, shelf_current_weight, shelf_current_volume = unpack_shelf_info(shelf_info)

        new_cap_valid, shelf_new_weight, shelf_new_volume = shelf_capacity_calculate(shelf_weight_cap,shelf_current_weight,product_weight,shelf_volume_cap,shelf_current_volume,product_volume,"decrease")

        if not new_cap_valid:
            return False

        if product_current_volume < prod["product_volume"]:
            print(f"\n[BANCO DE DADOS - CHECAGEM DE PRODUTO] QUANTIDADE DO PEDIDO INFERIO AO DISPONÍVEL EM ESTOQUE.\n")
            return False

        product_new_volume = product_current_volume - prod["product_volume"]
        
        product_order = {
            "id":prod["id"],
            "new_product_volume":product_new_volume,
            "cabinet_shelf_id":shelf_id,
            "new_shelf_weight":shelf_new_weight,
            "new_shelf_volume":shelf_new_volume,
        }

        final_cart.append(product_order)

    # print(product_order)
    
    result = inv_dao.checkout_cart(final_cart)

    return result









#region TESTS AREA
def test_check_order():
    cart = [
        {
            "id":8,
            "product_volume":1,
            "cabinet_shelf_id":5,
        }
    ]

    result = checkout_cart(cart)

    print(result)

    pass

# def test_new_product():
#     from server.core.models.products_list_test import products_list as lists

#     cart_list = lists[-1]
#     print(cart_list)

#     # print(cart)
#     # cart_list = list(cart.values())

#     result = new_product(*cart_list.values())

#     print(result)





#endregion