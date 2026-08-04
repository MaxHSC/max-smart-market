payment_dict = {}

def request_payment_order(order_number: int,total_order_price: float) -> dict:
    payment_dict.setdefault(order_number,{})["total_order_price"] = total_order_price

    return payment_dict

def confirm_payment(order_number,total_order_price,inserted_value) -> tuple:
    if inserted_value != total_order_price:
        return False, order_number

    return True, order_number