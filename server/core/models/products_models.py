from datetime import datetime, timedelta

from server.database import hardware_dao as hard_dao
from server.database import inventory_dao as inv_dao

#region MATHS OPERATIONS
def shelf_capacity_calculate(total_weight_cap,current_weight,delta_weight,total_volume_cap,current_volume,delta_volume,command) -> tuple:
    #CALCULATE CURRENT SHELF CAPACITY WEIGHT AND VOLUME
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


def unpack_shelf_info(shelf_info: dict) -> tuple:
    shelf_weight_cap = shelf_info["weight_capacity_grams"]
    shelf_volume_cap = shelf_info["volume_capacity"]

    shelf_current_weight = shelf_info["current_weight_grams"] if shelf_info["current_weight_grams"] is not None else 0
    shelf_current_volume = shelf_info["current_volume"] if shelf_info["current_volume"] is not None else 0

    return shelf_weight_cap, shelf_volume_cap, shelf_current_weight, shelf_current_volume

def current_shelf_values(order: list) -> tuple: #RETURN SHELF LIST WITH CURRENT DATABASE VALUES
    current_shelfs_values_list = []
    shelf_cabinet_id_list = []
    cabinet_id_list = []

    processed_shelfs = set() #ONLY FOR THE NEXT FOR LOOP

    for prod in order[1:]: #GET CURRENT DATABASE SHELFS VALUES
        _, _, _, shelf_id = inv_dao.get_product_info(prod["id"])
        
        shelf_info = hard_dao.search_shelf_id(shelf_id)

        if not shelf_id in processed_shelfs:
            shelf_weight_cap = shelf_info["weight_capacity_grams"]
            shelf_volume_cap = shelf_info["volume_capacity"]
            current_shelf_weight = shelf_info["current_weight_grams"]
            current_shelf_volume = shelf_info["current_volume"]

            cabinet_id_list.append(shelf_info["installed_cabinet_id"])

            current_shelfs_values_list.append(
                {
                    "cabinet_shelf_id":shelf_id,
                    "shelf_weight_cap":shelf_weight_cap,
                    "shelf_volume_cap":shelf_volume_cap,
                    "current_shelf_weight":current_shelf_weight,
                    "current_shelf_volume":current_shelf_volume
                }
            )

            processed_shelfs.add(shelf_id)

    return current_shelfs_values_list, cabinet_id_list


def available_products_calc(products_stock: list, products_reserved: dict) -> list[dict]:
    '''
    REFATOR THIS FEATURE TO MAKE A INDEX OF ONLY RESERVED PRODUCTS ID LOCATED BY INDEX IN THE INDEX LIST, DOING THE LOOP ITERATES DIRECTLY INTO THESE INDEX LIKE for prod in products_stock[1,4,37,345] THIS TUPLE WILL BE CREATED FROM THE RESERVED PRODUCTS LIST
    '''
    for prod in products_stock:
        if prod["id"] in products_reserved:
            prod["product_volume"] = prod["product_volume"] - products_reserved[prod["id"]]
    
    return products_stock


def get_values_from_shelf_list(current_shelf_values_list: list, shelf_id) -> tuple:
    for shelf in current_shelf_values_list:
        if shelf["cabinet_shelf_id"] == shelf_id:
            shelf_weight_cap = shelf["shelf_weight_cap"]
            shelf_volume_cap = shelf["shelf_volume_cap"]
            current_shelf_weight = shelf["current_shelf_weight"]
            current_shelf_volume = shelf["current_shelf_volume"]
            break
    
    return shelf_weight_cap, shelf_volume_cap, current_shelf_weight, current_shelf_volume


def get_new_shelfs_values(current_shelf_values_list: list,shelf_id: int,new_shelf_weight: float,new_shelf_volume: int) -> list[dict]:
    for shelf in current_shelf_values_list:
        if shelf["cabinet_shelf_id"] == shelf_id:
            shelf["new_shelf_weight"] = new_shelf_weight
            shelf["new_shelf_volume"] = new_shelf_volume
            break
    
    return current_shelf_values_list

def calculate_products_and_shelfs_volumes_weight(order: list, current_shelf_values_list: list) -> tuple:
    final_order = []
    for prod in order[1:]:
        reserved, product_stock_volume, product_weight, shelf_id = inv_dao.get_product_info(prod["id"])

        available_product_volume = product_stock_volume - reserved
        
        if not available_product_volume:
            return ()
        
        product_volume = prod["product_volume"]

        shelf_weight_cap, shelf_volume_cap, current_shelf_weight, current_shelf_volume = get_values_from_shelf_list(current_shelf_values_list,shelf_id)

        check_new_cap_valid, new_shelf_weight, new_shelf_volume = shelf_capacity_calculate(shelf_weight_cap,current_shelf_weight,product_weight,shelf_volume_cap,current_shelf_volume,product_volume,"decrease")

        if not check_new_cap_valid:
            return ()

        new_shelfs_values_list = get_new_shelfs_values(current_shelf_values_list,shelf_id,new_shelf_weight,new_shelf_volume)

        if available_product_volume < product_volume:
            print(f"\n[BANCO DE DADOS - CHECAGEM DE PRODUTO] QUANTIDADE DO PEDIDO SUPERIOR AO DISPONÍVEL EM ESTOQUE.\n")
            return ()

        new_product_volume = available_product_volume - prod["product_volume"]
        
        product_order = {
            "product_id":prod["id"],
            "new_product_volume":new_product_volume,
            "cabinet_shelf_id":shelf_id
        }

        final_order.append(product_order)

    return final_order, new_shelfs_values_list


def calculate_prices(order: list) -> None:
    order_products_list = []
    for prod in order[1:]:
        order_products_list.append(prod["product_id"])
    
    products_prices_dict: dict = inv_dao.get_products_prices(order_products_list)

    order[0]["total_order_price"] = sum(products_prices_dict.values())

    for prod in order[1:]:
        prod["product_unit_price"] = products_prices_dict[prod["product_id"]]
        prod["product_total_price"] = prod["product_unit_price"] * prod["product_volume"]
    
    return


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


def change_product_info(product_info,selected_column,new_value,command=None,product_weight=None,shelf_id=None,shelf_new_weight=None,shelf_new_volume=None) -> bool:
    product_id = product_info["id"]

    if command:
        shelf_id = product_info["cabinet_shelf_id"]
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

    return result


def get_products_list():
    '''
    THIS FUNCTION GET PRODUCTS IN STOCK AND RESERVED PRODUCTS IF "PENDENTE" AND MAKE THE MATHS WITH products_stock - products_reserved TO RETURN A AVAILABLE PRODUCTS LIST
    '''
    products_stock, products_reserved = inv_dao.list_all_products()
    '''
    products_reserved IS A DICT WITH product_id AS THE KEY AND amount_reserved AS THE VALUE'''

    available_products_list = available_products_calc(products_stock,products_reserved)

    return available_products_list


def reserve_order(order: list) -> tuple: #RECEIVE FROM CONTROLLER (FROM VIEWS)
    order_number = inv_dao.get_last_order_number() + 1
    total_order_price = calculate_prices(order)

    created_order_time = datetime.now()
    expires_order_time = created_order_time + timedelta(minutes=order[0]["expires_time"])
    expires_order_time_str = expires_order_time.strftime("%Y-%m-%d %H:%M:%S")

    order[0]["order_number"] = order_number
    user_id = order[0]["user_id"]
    expires_time = order[0]["expires_time"]
    order[0]["total_order_price"] = total_order_price

    for prod in order[1:]:
        prod["order_number"] = order_number
        prod["user_id"] = user_id
        prod["expires_time"] = expires_time
        
    
    confirm_reservation = inv_dao.reserve_order(order) #SEND TO INVENTORY DAO (RESERVATION TABLE)

    if not confirm_reservation:
        return False, False, False
    
    return order_number, expires_time, user_id, total_order_price #RETURN TO CONTROLLER (TO GATEWAY PAYMENT)


def expires_order(order_number: int, user_id) -> bool:
    order_expired = inv_dao.expires_order(order_number)

    return order_expired


def cancel_order(order_number: int) -> bool: #RECEIVE FROM CONTROLLER (FROM VIEWS)
    order_cancelled = inv_dao.cancel_order(order_number)

    return order_cancelled


def restore_order(order_number: int, user_id: int) -> tuple: #RECEIVE FROM CONTROLLER (FROM GATEWAY PAYMENT)
    order = inv_dao.restore_order(order_number)

    if not order:
        return ()
    
    order.insert(
        0,
        {
            "user_id": user_id,
            "order_number":order_number
        }
    )

    return order, order_number #RETURN TO CONTROLLER (TO CHECKOUT ORDER, THIS MODELS)


def checkout_order(order: list, order_number: int) -> tuple: #RECEIVE FROM CONTROLLER (FROM THIS MODELS AFTER ORDER RESTAURATION)
    current_shelf_values_list, cabinet_id_list = current_shelf_values(order) 

    final_order, new_shelfs_values_list = calculate_products_and_shelfs_volumes_weight(order,current_shelf_values_list)
    
    result = inv_dao.conclude_checkout_order(final_order,new_shelfs_values_list,order_number)

    return result, new_shelfs_values_list, order_number, cabinet_id_list #RETURN TO CONTROLLER (TO GENERATE TOKEN AND SEND TOKEN UNLOCK TO CABINETS AND TO WITHDRAWAL AUDIT)




'''cart ALWAYS MUST TO BE RECEIVED AS A LIST OF DICT WITH ID AND VOLUME TO BE BOUGHT
[   
    {
        "user_id":25,
        "expires_time":5,
    },
    {
        "id":19,
        "product_volume":3,
    },
]
AND SEND WITH NEW STOCK VALUES AND CART DICT
[
    {"id":19,
    "new_product_volume":3,
    "cabinet_shelf_id":5,
    "new_shelf_weight":15.0,
    "new_shelf_volume":15,
    "client_id":25
    },
]
'''



#region TESTS AREA
# def test_check_order():
#     cart = [
#         {
#             "id":8,
#             "product_volume":1,
#             "cabinet_shelf_id":5,
#         }
#     ]

#     result = checkout_cart(cart)

#     print(result)

#     pass

# def test_new_product():
#     from server.core.models.products_list_test import products_list as lists

#     cart_list = lists[-1]
#     print(cart_list)

#     # print(cart)
#     # cart_list = list(cart.values())

#     result = new_product(*cart_list.values())

#     print(result)





#endregion