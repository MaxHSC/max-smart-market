from server.database import inventory_dao as inv_dao, hardware_dao as hard_dao
from server.core.gateways import payment_gateway_simulator as pay_gat
from server.core.models import temp_products_models as prod_mod
from server.core.models import token_generator as token_gen
from server.core.models import temp_hardware_models as hard_mod
from server.core.validators import shopping_validators as serv_val
from server.core.calculations import calculations as calcs

# TODO: [Refatoração Futura - Arquitetura & Padronização]
    # 1. Avaliar evolução para 'Anemic Service': centralizar aqui a orquestração do ecossistema 
    #    (ex: disparar sockets para o hardware/armário físico após o retorno positivo do 'prod_mod').
    # 2. Agrupar os 8 parâmetros individuais em uma estrutura de dados unificada (ex: dict/DTO) 
    #    apenas quando o fluxo de rede (Network/Controller) estiver totalmente consolidado.

    #services será um worker que irá orquestrar a comunicação entre os módulos, validando as informações e chamando os métodos dos modelos e gateways de acordo com os pacotes recebidos.

class ProductsServices():
    def __init__(self):
        self.action_mapping ={
            "NEW_PRODUCT": self.new_product,
            "CHANGE_PRODUCT_INFO": self.change_product_info,
        }

#region GENERAL UTILS
    def process_payload(self, payload: dict):
        validation_result = serv_val.payload_validation(payload)

        if not validation_result:
            return False
        
        payload_action = payload["header"]["action"]

        action_target = self.action_mapping[payload_action]

        header: dict = payload["header"]
        body_payload: dict = payload["payload"]

        action_result = action_target(header,body_payload)

        return action_result


    def get_shelf_object(self,header:dict,body_payload:dict) -> hard_mod.InstalledShelf | None:
        shelf_info: dict = hard_dao.get_shelf_info(body_payload["shelf_id"])

        if shelf_info is None:
            return None

        shelf_object: hard_mod.InstalledShelf = hard_mod.InstalledShelf(shelf_info)

        return shelf_object

    def get_product_real_stock_object(self, header: dict, body_payload: dict) -> prod_mod.RealStockProduct | None:
        product_info: dict | None = inv_dao.get_product_real_stock_info(body_payload)

        if product_info is None:
            return None
        
        real_stock_product_object: prod_mod.RealStockProduct = prod_mod.RealStockProduct(product_info)

        return real_stock_product_object

    def attributes_to_dict(self,self_object, fields: list[str]) -> dict:
        object_dict: dict = {}

        for field in fields:
            object_dict[field] = getattr(self_object,field)
        
        return object_dict
#endregion


#region NEW PRODUCT
    def new_product(self, header:dict, body_payload: dict) -> bool: #MÉTODO QUE RECEBE EXTERNO E ENVIA INTERNO
        item: dict = body_payload["item"]

        new_product_object: prod_mod.NewProduct = prod_mod.NewProduct(item)
        if new_product_object is None:
            return False

        shelf_object: hard_mod.InstalledShelf | None = self.get_shelf_object(header,body_payload=item)
        if shelf_object is None:
            return False

#region CALCS
        volume_result = calcs.shelf_volume_calculation(shelf_object, new_product_object)
        if not volume_result:
            return False
    
        shelf_object.current_volume = shelf_object.current_volume + new_product_object.product_volume
        
        weight_result = calcs.shelf_weight_calculation(shelf_object, new_product_object)
        if not weight_result:
            return False
        
        shelf_object.current_weight_grams = shelf_object.current_weight_grams + (new_product_object.product_weight * new_product_object.product_volume)
#endregion

#region MOUNT DICT
        new_product_attributes_list = ["product_name", "bar_code", "price", "product_batch", "validity", "product_weight", "shelf_id", "product_volume"]
        shelf_attributes_list = ["current_weight_grams", "current_volume", "id"]

        new_product_dict: dict = self.attributes_to_dict(new_product_object,new_product_attributes_list)
        update_shelf_dict: dict = self.attributes_to_dict(shelf_object, shelf_attributes_list)

        result = inv_dao.add_new_product(new_product_dict, update_shelf_dict)

        return result
#enderion

#region CHANGE PRODUCT
    def change_product_info(self,header: dict, body_payload: dict) -> bool: #MÉTODO QUE RECEBE EXTERNO E ENVIA INTERNO
        item: dict = body_payload["item"]
        update_shelf_dict: dict = {}

        real_stock_product_object: prod_mod.RealStockProduct | None = self.get_product_real_stock_object(header,body_payload=item)

        if real_stock_product_object is None:
            return False

        shelf_object: hard_mod.InstalledShelf | None = self.get_shelf_object(header,body_payload=item)

        if shelf_object is None:
            return False
#region CALCS
        if item["column_to_change"] == "product_volume":
            shelf_new_volume = calcs.new_shelf_volume(shelf_object,real_stock_product_object,item)
            shelf_new_weight = calcs.new_shelf_weight(shelf_object,real_stock_product_object,item)

            if not shelf_new_volume or not shelf_new_weight:
                return False
      
            shelf_object.current_volume = shelf_new_volume
            shelf_object.current_weight_grams = shelf_new_weight

            shelf_attributes_list = ["current_weight_grams", "current_volume", "id"]
            update_shelf_dict: dict = self.attributes_to_dict(shelf_object, shelf_attributes_list)
#endregion
#region MOUNT DICT
        setattr(real_stock_product_object, item["column_to_change"], item["new_value"])

        product_attributes_list = ["product_id", "product_name", "price", "product_volume", "available"]

        update_product_dict: dict = self.attributes_to_dict(real_stock_product_object, product_attributes_list)
        
        result = inv_dao.change_product_info(update_product_dict,update_shelf_dict)

        return result
#endregion

#region ACTIONS RESERVE
    # def reserve_order(self,header: dict, body_payload: dict) -> tuple: #MÉTODO QUE RECEBE EXTERNO E ENVIA INTERNO
    #     items: list[dict] = body_payload["items"]
    #     real_stock_products_object = []

    #     for product in items:
    #         product_object = prod_mod.RealStockProduct = self.get_product_real_stock_object(header,product)
    #         real_stock_products_object.append(product_object)
            
            

    #     if not validation_result:
    #         return None, None, None, None

    #     order_number, expires_time, user_id, total_order_price = prod_mod.reserve_order(order)

    #     return order_number, expires_time, user_id, total_order_price

    # def request_payment_order(self,order_number,total_order_price) -> dict: #MÉTODO QUE RECEBE INTERNO E ENVIA EXTERNO PARA O GATEWAY DE PAGAMENTO
    #     payment_dict = pay_gat.request_payment_order(order_number,total_order_price)

    #     return payment_dict #ENVIAR O DICIONÁRIO PARA O GATEWAY DE PAGAMENTO, QUE IRÁ GERAR O PEDIDO DE PAGAMENTO E RETORNAR UM STATUS DE CONFIRMAÇÃO.

    # def confirm_payment_order(self,order_number,total_order_price,inserted_value) -> tuple: #MÉTODO QUE RECEBE EXTERNO DO GATEWAY DE PAGAMENTO E ENVIA INTERNO PARA RESTORE
    #     validation_result = serv_val.confirm_payment_validation(order_number,total_order_price,inserted_value)

    #     if not validation_result:
    #         return (False, order_number)

    #     confirm_payment = pay_gat.confirm_payment(order_number,total_order_price,inserted_value)

    #     return confirm_payment

    # def restore_order(self,order_number: int, user_id: int) -> tuple: #MÉTODO QUE RECEBE INTERNO E ENVIA INTERNO
    #     order, order_number = prod_mod.restore_order(order_number,user_id)
        
    #     return order, order_number

    # def checkou_order(self,order: list, order_number: int) -> tuple: #MÉTODO RECEBE INTERNO E ENVIA INTERNO
    #     result, new_shelfs_values_list, order_number, cabinet_id_list = prod_mod.checkout_order(order,order_number)

    #     return result, new_shelfs_values_list, order_number, cabinet_id_list

    # def generate_token(self): #MÉTODO QUE RECEBE INTERNO E ENVIA INTERNO
    #     order_token, expires_token = token_gen.generate_token()

    #     return order_token, expires_token

    # def mount_token_payload(self,order_token: str, expires_token) -> bytes: #MÉTODO QUE RECEBE INTERNO E ENVIA INTERNO
    #     payload_package = token_gen.mount_token_payload(order_token,expires_token)

    #     return payload_package

    # def send_token_to_cabinet(self,payload_package, cabinet_list: list): #MÉTODO QUE RECEBE INTERNO E ENVIA EXTERNO PARA O CABINET E PARA O VIEWS
    #     #BUILD NETWORK TO SEND THIS PAYLOAD


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
#       { "product_id": 104, "requested_volume": 2 }
#     ],
#     "payment_method": "PIX"
#   }
# }

# def test_new_products_allocation():
#     # Payload modelo padrão do sistema
#     sample_payload = {
#         "header": { 
#             "correlation_id": "req_8f3a9b1c-2026",
#             "client_type": "totem",
#             "client_id": "TOTEM_LOJA_01",
#             "user_id": "3",
#             "role": "employee", 
#             "auth_token": "bearer.jwt.token.here",
#             "action": "NEW_PRODUCT",
#             "timestamp": "1785816136"
#         },
#         "payload": {
#             "item": {
#                 "bar_code": "",
#                 "product_name": "",
#                 "price": 0.0,
#                 "product_batch": "",
#                 "validity": "",
#                 "product_weight": 0.0,
#                 "shelf_id": 1,
#                 "product_volume": 1.0
#             }
#         }
#     }

#     # Instanciando a classe correta de serviços de produto
#     product_obj = ProductsServices()

#     # Matriz com 20 produtos prontos para inserção nas 15 prateleiras distintas
#     products_pool = [
#         {"bar_code": "7891000100010", "name": "Refrigerante Cola 2L", "price": 8.99, "batch": "LT-A1", "validity": "2027-01-15", "weight": 2000.0, "shelf_id": 1},
#         {"bar_code": "7891000100010", "name": "Refrigerante Cola 2L", "price": 8.99, "batch": "LT-A1", "validity": "2027-01-15", "weight": 2000.0, "shelf_id": 2},
#         {"bar_code": "7891000100010", "name": "Refrigerante Cola 2L", "price": 8.99, "batch": "LT-A2", "validity": "2027-02-20", "weight": 2000.0, "shelf_id": 3},
#         {"bar_code": "7891000100020", "name": "Leite Integral 1L", "price": 4.50, "batch": "LT-B1", "validity": "2026-11-05", "weight": 1000.0, "shelf_id": 4},
#         {"bar_code": "7891000100020", "name": "Leite Integral 1L", "price": 4.50, "batch": "LT-B1", "validity": "2026-11-05", "weight": 1000.0, "shelf_id": 5},
        
#         {"bar_code": "7891000100030", "name": "Arroz Integral 1kg", "price": 6.20, "batch": "LT-C1", "validity": "2027-08-12", "weight": 1000.0, "shelf_id": 6},
#         {"bar_code": "7891000100030", "name": "Arroz Integral 1kg", "price": 6.20, "batch": "LT-C1", "validity": "2027-08-12", "weight": 1000.0, "shelf_id": 7},
#         {"bar_code": "7891000100040", "name": "Feijão Preto 1kg", "price": 7.99, "batch": "LT-D1", "validity": "2027-06-18", "weight": 1000.0, "shelf_id": 8},
#         {"bar_code": "7891000100040", "name": "Feijão Preto 1kg", "price": 7.99, "batch": "LT-D2", "validity": "2027-07-01", "weight": 1000.0, "shelf_id": 9},
#         {"bar_code": "7891000100050", "name": "Café Torrado 500g", "price": 15.30, "batch": "LT-E1", "validity": "2027-04-30", "weight": 500.0, "shelf_id": 10},
        
#         {"bar_code": "7891000100050", "name": "Café Torrado 500g", "price": 15.30, "batch": "LT-E1", "validity": "2027-04-30", "weight": 500.0, "shelf_id": 11},
#         {"bar_code": "7891000100060", "name": "Chocolate Barra 90g", "price": 5.49, "batch": "LT-F1", "validity": "2027-10-10", "weight": 90.0, "shelf_id": 12},
#         {"bar_code": "7891000100060", "name": "Chocolate Barra 90g", "price": 5.49, "batch": "LT-F1", "validity": "2027-10-10", "weight": 90.0, "shelf_id": 13},
#         {"bar_code": "7891000700070", "name": "Azeite Oliva 500ml", "price": 34.90, "batch": "LT-G1", "validity": "2028-03-15", "weight": 500.0, "shelf_id": 14},
#         {"bar_code": "7891000700070", "name": "Azeite Oliva 500ml", "price": 34.90, "batch": "LT-G1", "validity": "2028-03-15", "weight": 500.0, "shelf_id": 15},
        
#         # Inserções repetidas para acumular peso/itens nas prateleiras existentes
#         {"bar_code": "7891000100010", "name": "Refrigerante Cola 2L", "price": 8.99, "batch": "LT-A1", "validity": "2027-01-15", "weight": 2000.0, "shelf_id": 1},
#         {"bar_code": "7891000100010", "name": "Refrigerante Cola 2L", "price": 8.99, "batch": "LT-A1", "validity": "2027-01-15", "weight": 2000.0, "shelf_id": 2},
#         {"bar_code": "7891000200099", "name": "Saco Batata G 25kg", "price": 49.90, "batch": "LT-X1", "validity": "2026-10-01", "weight": 25000.0, "shelf_id": 3}, # Ultrapassa limite de 20kg da prateleira 3
#         {"bar_code": "7891000100020", "name": "Leite Integral 1L", "price": 4.50, "batch": "LT-B1", "validity": "2026-11-05", "weight": 1000.0, "shelf_id": 4},
#         {"bar_code": "7891000100020", "name": "Leite Integral 1L", "price": 4.50, "batch": "LT-B2", "validity": "2026-11-20", "weight": 1000.0, "shelf_id": 5}
#     ]

#     for index, item_data in enumerate(products_pool):
#         # Mapeia dinamicamente cada atributo para o dicionário interno do payload
#         sample_payload["payload"]["item"]["bar_code"] = item_data["bar_code"]
#         sample_payload["payload"]["item"]["product_name"] = item_data["name"]
#         sample_payload["payload"]["item"]["price"] = item_data["price"]
#         sample_payload["payload"]["item"]["product_batch"] = item_data["batch"]
#         sample_payload["payload"]["item"]["validity"] = item_data["validity"]
#         sample_payload["payload"]["item"]["product_weight"] = item_data["weight"]
#         sample_payload["payload"]["item"]["shelf_id"] = item_data["shelf_id"]

#         # Dispara o processamento do payload através da camada de produtos
#         result = product_obj.process_payload(sample_payload)
        
#         # Exibe detalhadamente a operação no terminal
#         print(f"[Item {index + 1}/20] Inserindo '{item_data['name']}' na Shelf {item_data['shelf_id']} -> Resultado: {result}", flush=True)
