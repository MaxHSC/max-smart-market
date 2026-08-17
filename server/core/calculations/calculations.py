def shelf_volume_calculation(shelf_object, product_object):
    if shelf_object.current_volume + product_object.product_volume > shelf_object.volume_capacity or shelf_object.current_volume + product_object.product_volume <= 0:
        return False

    return True

def shelf_weight_calculation(shelf_object, product_object):
    if shelf_object.current_weight_grams + (new_product_object.product_weight * new_product_object.product_volume) > shelf_object.weight_capacity_grams or shelf_object.current_weight_grams + (new_product_object.product_weight * new_product_object.product_volume) <= 0:
        return False

    return True
    
def new_shelf_volume(shelf_object, real_stock_product_object, item):
    shelf_delta_volume = shelf_object.current_volume - real_stock_product_object.product_volume
    shelf_new_volume = shelf_delta_volume + item["new_value"]

    if shelf_new_volume > shelf_object.volume_capacity:
        return False
    
    return shelf_new_volume

def new_shelf_weight(shelf_object, real_stock_product_object, item):
    shelf_delta_weight = shelf_object.current_weight_grams - (real_stock_product_object.product_weight * real_stock_product_object.product_volume)
    shelf_new_weight = shelf_delta_weight + (real_stock_product_object.product_weight * item["new_value"])

    if shelf_new_weight > shelf_object.weight_capacity_grams:
        return False

    return shelf_new_weight

def product_available_volume_calculation(order_products_list,real_stock_products_mapping,reserved_products_mapping):
    for order_product in order_products_list: #CALCULO DE PRODUTOS DISPONIVEIS
        real_object: prod_mod.RealStockProduct | None = real_stock_products_mapping.get(order_product.id)

        reserved_volume = 0

        if real_object is None:
            return False

        if real_object:
            reserved_volume = reserved_products_mapping.get(order_product.id, 0)
        
        avaliable_volume = real_object.product_volume - reserved_volume

        if avaliable_volume < order_product.requested_volume:
            return False
        
    return True

def shelf_available_volume_weight_calculation():
    if shelf_object.current_volume - order_product.requested_volume > shelf_object.volume_capacity or shelf_object.current_volume - order_product.requested_volume < 0:
        return False
    
    if shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume) > shelf_object.weight_capacity_grams or shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume) < 0:
        return False

    return True

def price_calculation(order_products_list,real_stock_products_mapping):
    total_order_price: float = 0
    product_total_price = []
    product_unit_price = []

    for order_product in order_products_list:
        real_object = real_stock_products_mapping.get(order_product.id)

        if real_object is None:
            return None, [], []

        total_order_price += real_object.price * order_product.requested_volume
        product_total_price.append(
            {
                real_object.id: real_object.price*order_product.requested_volume
            }
        )
        product_unit_price.append(
            {
                real_object.id: real_object.price
            }
        )
    
    return total_order_price, product_total_price, product_unit_price