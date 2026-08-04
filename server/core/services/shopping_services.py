from server.core.gateways import payment_gateway_simulator as pay_gat
from server.core.models import products_models as prod_mod
from server.core.models import token_generator as token_gen


class ProductsServices():
    def __init__(self):
        self.order_number = None
        self.order = []


    def reserve_order(self,order: list) -> tuple:
        order_number, expires_time, user_id, total_order_price = prod_mod.reserve_order(order)

        return order_number, expires_time, user_id, total_order_price

    def request_payment_order(self,order_number,total_order_price) -> dict:
        payment_dict = pay_gat.request_payment_order(order_number,total_order_price)

        return payment_dict

    def confirm_payment_order(self,order_number,total_order_price,inserted_value) -> tuple:
        confirm_payment = pay_gat.confirm_payment(order_number,total_order_price,inserted_value)

        return confirm_payment

    def restore_order(self,order_number: int, user_id: int) -> tuple:
        order, order_number = prod_mod.restore_order(order_number,user_id)
        
        return order, order_number

    def checkou_order(self,order: list, order_number: int) -> tuple:
        result, new_shelfs_values_list, order_number, cabinet_id_list = prod_mod.checkout_order(order,order_number)

        return result, new_shelfs_values_list, order_number, cabinet_id_list

    def generate_token(self,order_number: int, cabinet_id_list: list):
        order_token, expires_token = token_gen.generate_token()

        return order_token, expires_token

    def mount_token_payload(self,order_token: str, expires_token, cabinet_id_list: list) -> bytes:
        payload_package = token_gen.mount_token_payload(order_token,expires_token)

        return payload_package

    def send_token_to_cabinet(self,payload_package, cabinet_list: list):
        #BUILD NETWORK TO SEND THIS PAYLOAD