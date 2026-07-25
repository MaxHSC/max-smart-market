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