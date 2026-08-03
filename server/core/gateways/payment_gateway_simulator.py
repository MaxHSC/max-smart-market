class POSDevice():
    def __init__(self):
        self.payment_value = 0.0
        self.payment_status = False
        self.payment_dict = {}
    
    def request_payment_order(self,order_number,total_order_price) -> dict:
        self.payment_dict.setdefault(order_number,{}) = {"total_order_price":total_order_price}

        return self.payment_dict
    
    def confirm_payment(self,order_number,total_order_price,inserted_value) -> tuple:
        if inserted_value != total_order_price:
            return False, order_number

        return True