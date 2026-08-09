from server.core.gateways import payment_gateway_simulator as pay_gat
from server.core.models import temp_products_models as prod_mod
from server.core.models import token_generator as token_gen
from server.core.validators import shopping_validators as serv_val
from server.core.calculations import products_calculations as prod_calc

# TODO: [Refatoração Futura - Arquitetura & Padronização]
    # 1. Avaliar evolução para 'Anemic Service': centralizar aqui a orquestração do ecossistema 
    #    (ex: disparar sockets para o hardware/armário físico após o retorno positivo do 'prod_mod').
    # 2. Agrupar os 8 parâmetros individuais em uma estrutura de dados unificada (ex: dict/DTO) 
    #    apenas quando o fluxo de rede (Network/Controller) estiver totalmente consolidado.

    #services será um worker que irá orquestrar a comunicação entre os módulos, validando as informações e chamando os métodos dos modelos e gateways de acordo com os pacotes recebidos.

class ProductsServices():
    def __init__(self):
        self.order_number = None
        self.order = []
        self.action_mapping ={
            "NEW_PRODUCT": self.new_product,
            "CHANGE_PRODUCT_INFO": change_product_info_validation,
            "ORDER_CREATE": reserve_order_validation,
            "ORDER_CANCEL": cancel_order_validation,
            "ORDER_RESTORE": restore_order_validation,
            "SUSPEND_PRODUCT": suspend_product_validation,
            "UNSUSPEND_PRODUCT": unsuspend_product_validation,
            "GET_PRODUCTS_LIST": get_products_list_validation,
            "GET_PRODUCT_INFO": get_product_info_validation,
        }

    def process_payload(self, payload: dict):
        validation_result = serv_val.new_product_validation(payload)

        if not validation_result:
            return False
        
        payload_action = payload["header"]["action"]

        action_result = self.action_mapping(payload_action)

        return action_result



    def new_product(self,payload: dict) -> bool: #MÉTODO QUE RECEBE EXTERNO E ENVIA INTERNO
        new_product_object = prod_mod.Product()
        result = prod_mod.new_product(bar_code, product_name, price, product_batch, validity, product_weight, cabinet_shelf_id, product_volume)

        return result

    def change_product_info(self,product_info,selected_column,new_value,command=None,product_weight=None) -> bool: #MÉTODO QUE RECEBE EXTERNO E ENVIA INTERNO
        validation_result = serv_val.change_product_info_validation(selected_column, new_value)

        if not validation_result:
            return False

        result = prod_mod.change_product_info(product_info,selected_column,new_value,command,product_weight)

        return result

    def reserve_order(self,order: list) -> tuple: #MÉTODO QUE RECEBE EXTERNO E ENVIA INTERNO
        validation_result = serv_val.reserve_oder_validation(order) #ALTERAR O QUE ENVIAR PARA A FUNÇÃO DE VALIDAÇÃO, POIS AINDA NÃO ESTÁ DEFINIDO O QUE SERÁ ENVIADO PARA A FUNÇÃO DE VALIDAÇÃO.

        if not validation_result:
            return None, None, None, None

        order_number, expires_time, user_id, total_order_price = prod_mod.reserve_order(order)

        return order_number, expires_time, user_id, total_order_price

    def request_payment_order(self,order_number,total_order_price) -> dict: #MÉTODO QUE RECEBE INTERNO E ENVIA EXTERNO PARA O GATEWAY DE PAGAMENTO
        payment_dict = pay_gat.request_payment_order(order_number,total_order_price)

        return payment_dict #ENVIAR O DICIONÁRIO PARA O GATEWAY DE PAGAMENTO, QUE IRÁ GERAR O PEDIDO DE PAGAMENTO E RETORNAR UM STATUS DE CONFIRMAÇÃO.

    def confirm_payment_order(self,order_number,total_order_price,inserted_value) -> tuple: #MÉTODO QUE RECEBE EXTERNO DO GATEWAY DE PAGAMENTO E ENVIA INTERNO PARA RESTORE
        validation_result = serv_val.confirm_payment_validation(order_number,total_order_price,inserted_value)

        if not validation_result:
            return (False, order_number)

        confirm_payment = pay_gat.confirm_payment(order_number,total_order_price,inserted_value)

        return confirm_payment

    def restore_order(self,order_number: int, user_id: int) -> tuple: #MÉTODO QUE RECEBE INTERNO E ENVIA INTERNO
        order, order_number = prod_mod.restore_order(order_number,user_id)
        
        return order, order_number

    def checkou_order(self,order: list, order_number: int) -> tuple: #MÉTODO RECEBE INTERNO E ENVIA INTERNO
        result, new_shelfs_values_list, order_number, cabinet_id_list = prod_mod.checkout_order(order,order_number)

        return result, new_shelfs_values_list, order_number, cabinet_id_list

    def generate_token(self): #MÉTODO QUE RECEBE INTERNO E ENVIA INTERNO
        order_token, expires_token = token_gen.generate_token()

        return order_token, expires_token

    def mount_token_payload(self,order_token: str, expires_token) -> bytes: #MÉTODO QUE RECEBE INTERNO E ENVIA INTERNO
        payload_package = token_gen.mount_token_payload(order_token,expires_token)

        return payload_package

    def send_token_to_cabinet(self,payload_package, cabinet_list: list): #MÉTODO QUE RECEBE INTERNO E ENVIA EXTERNO PARA O CABINET E PARA O VIEWS
        #BUILD NETWORK TO SEND THIS PAYLOAD


# payload_sample ={
#   "header": {
#     "correlation_id": "req_8f3a9b1c-2026",
#     "client_type": "totem",
#     "client_id": "TOTEM_LOJA_01",
#     "role": "consumer",
#     "auth_token": "bearer.jwt.token.here",
#     "action": "ORDER_CREATE",
#     "timestamp": 1785816136
#   },
#   "payload": {
#     "items": [
#       { "product_id": 104, "quantity": 2 }
#     ],
#     "payment_method": "PIX"
#   }
# }