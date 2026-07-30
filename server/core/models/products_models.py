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


def unpack_shelf_info(shelf_info: dict):
    shelf_weight_cap = shelf_info["weight_capacity_grams"]
    shelf_volume_cap = shelf_info["volume_capacity"]

    shelf_current_weight = shelf_info["current_weight_grams"] if shelf_info["current_weight_grams"] is not None else 0
    shelf_current_volume = shelf_info["current_volume"] if shelf_info["current_volume"] is not None else 0

    return shelf_weight_cap, shelf_volume_cap, shelf_current_weight, shelf_current_volume

def current_values_into_shelf_list(cart: list) -> list[Dict]: #RETURN SHELF LIST WITH CURRENT DATABASE VALUES
    shelfs_new_values_list = []
    shelfs_processed = set() #ONLY FOR THE FOR LOOP AHEAD

    for prod in cart: #GET CURRENT DATABASE SHELFS VALUES
        _, _, shelf_id = inv_dao.get_product_info(prod["id"])
        
        shelf_info = hard_dao.search_shelf_id(shelf_id)

        if not shelf_id in shelfs_processed:
            shelf_weight_cap = shelf_info["weight_capacity_grams"]
            shelf_volume_cap = shelf_info["volume_capacity"]
            shelf_current_weight = shelf_info["current_weight_grams"]
            shelf_current_volume = shelf_info["current_volume"]

            shelfs_new_values_list.append(
                {
                    "cabinet_shelf_id":shelf_id,
                    "shelf_weight_cap":shelf_weight_cap,
                    "shelf_volume_cap":shelf_volume_cap,
                    "new_shelf_weight":shelf_current_weight,
                    "new_shelf_volume":shelf_current_volume
                }
            )

            shelfs_processed.add(shelf_id)

    return shelfs_new_values_list

def get_values_from_shelf_list(shelfs_new_values: list, shelf_id):
    for shelf in shelfs_new_values:
        if shelf["cabinet_shelf_id"] == shelf_id:
            shelf_weight_cap = shelf["shelf_weight_cap"]
            shelf_volume_cap = shelf["shelf_volume_cap"]
            shelf_current_weight = shelf["new_shelf_weight"]
            shelf_current_volume = shelf["new_shelf_volume"]
            break
    
    return shelf_weight_cap, shelf_volume_cap, shelf_current_weight, shelf_current_volume


def get_shelfs_new_values(shelfs_new_values: list,shelf_id: int,shelf_new_weight: float,shelf_new_volume: int) -> list[Dict]:
    for shelf in shelfs_new_values:
        if shelf["cabinet_shelf_id"] == shelf_id:
            shelf["new_shelf_weight"] = shelf_new_weight
            shelf["new_shelf_volume"] = shelf_new_volume
            break
    
    return shelfs_new_values

def calculate_products_and_shelfs_volumes_weight(cart: list, shelfs_new_values_list: list) -> list:
    final_cart = []
    for prod in cart:
        product_current_volume, product_weight, shelf_id = inv_dao.get_product_info(prod["id"])
        
        if not product_current_volume:
            return False
        
        product_volume = prod["product_volume"]

        shelf_weight_cap, shelf_volume_cap, shelf_current_weight, shelf_current_volume = get_values_from_shelf_list(shelfs_new_values_list,shelf_id)

        check_new_cap_valid, shelf_new_weight, shelf_new_volume = shelf_capacity_calculate(shelf_weight_cap,shelf_current_weight,product_weight,shelf_volume_cap,shelf_current_volume,product_volume,"decrease")

        if not check_new_cap_valid:
            return False

        shelfs_new_values_list = get_shelfs_new_values(shelfs_new_values_list,shelf_id,shelf_new_weight,shelf_new_volume)

        if product_current_volume < product_volume:
            print(f"\n[BANCO DE DADOS - CHECAGEM DE PRODUTO] QUANTIDADE DO PEDIDO INFERIO AO DISPONÍVEL EM ESTOQUE.\n")
            return False

        product_new_volume = product_current_volume - prod["product_volume"]
        
        product_order = {
            "id":prod["id"],
            "new_product_volume":product_new_volume,
            "cabinet_shelf_id":shelf_id
        }

        final_cart.append(product_order)

    return final_cart, shelfs_new_values_list
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


def get_products_list():
    products_list = inv_dao.list_all_products()

    return products_list


def checkout_cart(cart: list):
    shelfs_new_values_list = current_values_into_shelf_list(cart)

    final_cart, shelfs_new_values = calculate_products_and_shelfs_volumes_weight(cart,shelfs_new_values_list)
    
    result = inv_dao.checkout_cart(final_cart,shelfs_new_values_list)

    return result

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