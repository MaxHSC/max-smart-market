from server.database import inventory_dao as inv_dao, hardware_dao as hard_dao
from server.core.models import temp_products_models as prod_mod
from server.core.models import temp_hardware_models as hard_mod
from server.core.validators import shopping_validators as serv_val
from server.core.calculations import calculations as calcs

from datetime import datetime, timedelta

class ShoppingServices:
    def __init__(self):
        self.action_mapping = {
            "ORDER_CREATE": self.reserve_order,
            "ORDER_RESTORE": self.restore_order,
            "ORDER_CANCEL": self.cancel_order,
            "GET_PRODUCTS_LIST": self.get_products_list,
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
    
    def get_product_reserved_stock_object(self, header: dict, product: dict) -> prod_mod.ReservedProduct | None:
        product_info: dict | None = inv_dao.get_product_reserved_stock_info(product)

        if product_info is None:
            return None
        
        reserved_product_object: prod_mod.ReservedProduct = prod_mod.ReservedProduct(product_info)

        return reserved_product_object

    def attributes_to_dict(self,self_object, fields: list[str]) -> dict:
        object_dict: dict = {}

        for field in fields:
            object_dict[field] = getattr(self_object,field)
        
        return object_dict
#endregion

#region RESERVE ORDER
    def reserve_order(self,header:dict,body_payload:dict):
        item_list: list[dict] = body_payload["items"]
        real_stock_products_object_list = []
        reserved_products_object_list = []
        order_products_list = []
        shelfs_object_list = []
        shelf_mapping = {}

#region INSTANTIATES OBJECT
        for product in item_list: #INSTANCIA PRODUTO EM ESTOQUE E RESERVADO E ADICIONA À LISTA
            real_product_object: prod_mod.RealStockProduct | None = self.get_product_real_stock_object(header,product)
            real_stock_products_object_list.append(real_product_object)

            reserved_product_object = self.get_product_reserved_stock_object(header,product)
            if reserved_product_object is not None:
                reserved_products_object_list.append(reserved_product_object)
            
            order_product_object: prod_mod.OrderProduct = prod_mod.OrderProduct(product)
            order_products_list.append(order_product_object)
        

        reserved_products_mapping = {reserved_object.id: reserved_object.reserved_volume for reserved_object in reserved_products_object_list} #MAPPPING DE PRODUTOS RESERVADOS

        real_stock_products_mapping = {real_object.id: real_object for real_object in real_stock_products_object_list} # MAPPING DE PRODUTOS EM ESTOQUE
#endregion

#region VOLUME AND WEIGHT
        available_volume = calcs.product_available_volume_calculation(order_products_list,real_stock_products_mapping,reserved_products_mapping)

        if not available_volume:
            return False

        for order_product in order_products_list: #CALCULO DE PESOS E VOLUMES EM RELACAO ÀS PRATELEIRAS
            real_object = real_stock_products_mapping.get(order_product.id)

            if real_object is None:
                return False

            shelf_id_dict = {"shelf_id":real_object.shelf_id}

            shelf_object = self.get_shelf_object(header,shelf_id_dict)
            shelfs_object_list.append(shelf_object)

            if shelf_object is None:
                return False

            if shelf_object.id not in shelf_mapping:
                shelf_mapping[shelf_object.id] = shelf_object
            
            available_volume_weight_shelf = calcs.shelf_available_volume_weight_calculation(shelf_object,real_object,order_product)

            if not available_volume_weight_shelf:
                return False
            
            shelf_object.current_volume = shelf_object.current_volume - order_product.requested_volume
            shelf_object.current_weight_grams = shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume)
#endregion

#region PRICES
        total_order_price, product_total_price, product_unit_price = calcs.price_calculation(order_products_list,real_stock_products_mapping)

        if total_order_price is None:
            return False
#endregion

#region INSTANTIATES ORDER
        created_order_time = datetime.now() #NÃO É DECLARADO, ASSUME VALOR DEFAULT NO DB
        expires_order_time = created_order_time + timedelta(minutes=10)
        created_order_time_str = created_order_time.strftime("%Y-%m-%d %H:%M:%S")
        expires_order_time_str = expires_order_time.strftime("%Y-%m-%d %H:%M:%S")

        order_number = inv_dao.get_last_order_number() + 1

        order_object: prod_mod.PurchaseOrder = prod_mod.PurchaseOrder(header,body_payload)
        order_object.order_number = order_number
        order_object.total_order_price = total_order_price
        order_object.product_total_price = product_total_price
        order_object.product_unit_price = product_unit_price
        order_object.created_time = created_order_time_str
        order_object.expires_time = expires_order_time_str
#endregion

#region MOUNT DICT
        order_list: list[dict] = []
        for product in order_object.product_id_list:
            order_list.append(
                {
                    "order_number": order_object.order_number,
                    "user_id": order_object.user_id,
                    "total_order_price": order_object.total_order_price,
                    "product_id": product["product_id"],
                    "product_unit_price": order_object.product_unit_price,
                    "product_total_price": order_object.product_total_price,
                    "reserved_volume": product["requested_volume"],
                    "created_time": order_object.created_time,
                    "expires_time": order_object.expires_time
                    

                }
            )
#endregion

#region PERSIST DB VIA DAO
        confirm_order_reservation: bool = inv_dao.reserve_order(order_list)

        if not confirm_order_reservation:
            return False
        
        return confirm_order_reservation
#endregion

#region RESTORE ORDER
    def restore_order(self,header:dict,body_payload:dict):
        order_restored: dict | None = inv_dao.restore_order(body_payload)
        real_stock_products_object_list = []
        reserved_products_object_list = []
        order_products_list = []
        shelfs_object_list = []
        new_shelfs_values = []
        shelf_mapping = {}

        if order_restored is None:
            return False

#region INSTANTIATES OBJECT
        order_object: prod_mod.PurchaseOrder = prod_mod.PurchaseOrder(header,order_restored)
        order_object.order_number = body_payload["order_number"]
        order_object.total_order_price = order_restored["total_order_price"]
        order_object.product_id_list = order_restored["items"]
        order_object.created_time = order_restored["created_time"]
        order_object.expires_time = order_restored["expires_time"]
        order_object.reserve_status = "CONCLUIDA"
        order_object.payment_status = "CONCLUIDA"

        for product in order_object.product_id_list: #INSTANCIA PRODUTO EM ESTOQUE E RESERVADOS E ADICIONA À LISTA
            real_product_object: prod_mod.RealStockProduct | None = self.get_product_real_stock_object(header,product)
            real_stock_products_object_list.append(real_product_object)

            reserved_product_object = self.get_product_reserved_stock_object(header,product)
            if reserved_product_object is not None:
                reserved_products_object_list.append(reserved_product_object)
            
            order_product_object: prod_mod.OrderProduct = prod_mod.OrderProduct(product)
            order_products_list.append(order_product_object)
        

        reserved_products_mapping = {reserved_object.id: reserved_object.reserved_volume for reserved_object in reserved_products_object_list} #MAPPPING DE PRODUTOS RESERVADOS

        real_stock_products_mapping = {real_object.id: real_object for real_object in real_stock_products_object_list} # MAPPING DE PRODUTOS EM ESTOQUE
#endregion

#region CALC PRODUCT VOL
        
        for order_product in order_products_list: #CALCULO QUE ATUALIZA VOLUME DOS PRODUTOS
            real_object: prod_mod.RealStockProduct | None = real_stock_products_mapping.get(order_product.id)

            if real_object is None:
                return False
            
            new_product_volume = real_object.product_volume - order_product.requested_volume

            if new_product_volume < 0 or new_product_volume > 20:
                return False

            real_object.product_volume = new_product_volume
        

        for order_product in order_products_list: #CALCULO DE PESOS E VOLUMES EM RELACAO ÀS PRATELEIRAS
            real_object = real_stock_products_mapping.get(order_product.id)

            if real_object is None:
                return False

            shelf_id_dict = {"shelf_id":real_object.shelf_id}

            shelf_object = self.get_shelf_object(header,shelf_id_dict)
            shelfs_object_list.append(shelf_object)

            if shelf_object is None:
                return False

            if shelf_object.id not in shelf_mapping:
                shelf_mapping[shelf_object.id] = shelf_object
            
            if shelf_object.current_volume - order_product.requested_volume > shelf_object.volume_capacity or shelf_object.current_volume - order_product.requested_volume < 0:
                return False
            
            if shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume) > shelf_object.weight_capacity_grams or shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume) < 0:
                return False
            
            shelf_object.current_volume = shelf_object.current_volume - order_product.requested_volume
            shelf_object.current_weight_grams = shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume)

        for shelf in shelfs_object_list:
            new_shelfs_values.append(
                {
                    "shelf_id": shelf.id,
                    "new_shelf_weight": shelf.current_weight_grams,
                    "new_shelf_volume": shelf.current_volume
                }
            )

        
        order_list: list[dict] = []
        for product_object in real_stock_products_object_list:
            order_list.append(
                {
                    "order_number": order_object.order_number,
                    "product_id": product_object.id,
                    "new_product_volume": product_object.product_volume,
                }
            )

        result = inv_dao.conclude_checkout_order(order_list,new_shelfs_values)

        if result is None:
            return False

        return result
#endregion

#region CANCEL ORDER
    def cancel_order(self, header: dict, body_payload: dict):
        result = inv_dao.cancel_order(body_payload)

        return result
    
#region PRODUCT LIST
    def get_products_list(header: dict, body_payload: dict) -> list[dict]:
        products_stock, products_reserved = inv_dao.list_all_products()

        for product in products_reserved:
            product_id = product["product_id"]

            if product_id in products_stock:
                products_stock[product_id]["product_volume"] -= product["reserved_volume"]
        
        products_list = list(products_stock.values())

        return products_list

# def test_new_order():
#     payload = {
#             "header": { 
#                 "correlation_id": "req_8f3a9b1c-2026",
#                 "client_type": "totem",
#                 "client_id": "TOTEM_LOJA_01",
#                 "user_id": "3",
#                 "role": "consumer", #consumer, employee, manager
#                 "auth_token": "bearer.jwt.token.here",
#                 "action": "ORDER_CREATE",
#                 "timestamp": "1785816136"
#             },
#             "payload": {
#                 "items": [
#                     {
#                         "product_id": 1,        # Arroz Integral 1kg
#                         "requested_volume": 2   # 2 unidades (Volume total: 2.4)
#                     },
#                     {
#                         "product_id": 3,        # Óleo de Soja 900ml
#                         "requested_volume": 3   # 3 unidades (Volume total: 2.7)
#                     },
#                     {
#                         "product_id": 6,        # Macarrão Espaguete
#                         "requested_volume": 5   # 5 unidades (Volume total: 3.0)
#                     },
#                     {
#                         "product_id": 8,        # Leite UHT Integral 1L
#                         "requested_volume": 4   # 4 unidades (Volume total: 4.0)
#                     },
#                     {
#                         "product_id": 10,       # Refrigerante Cola 2L
#                         "requested_volume": 2   # 2 unidades (Volume total: 4.0)
#                     },
#                     {
#                         "product_id": 16,       # Chocolate em Barra
#                         "requested_volume": 6   # 6 unidades (Volume total: 0.6)
#                     }
#                 ]
#             }
#     }

#      # Instanciando a classe correta de serviços de compras
#     shopping_obj = ShoppingServices() 

#     # Executa o fluxo enviando o payload para o processamento de compras
#     result = shopping_obj.process_payload(sample_payload)
    
#     # Exibe o resultado do teste no terminal de forma clara
#     print(f"\n[TESTE - PEDIDO] Criação da Ordem na ShoppingServices com 6 itens distintos -> Resultado: {result}", flush=True)

    


        #CONSIDERAR SALVAR NOVAS CAPS DE SHELF NO MÉTODO DE RESERVA, SALVANDO OS VALORES EM UMA LISTA QUE IRÁ PARA A ORDEM DE COMPRAS EM RESERVA, AO SER RESTAURADA, OS OBJETOS DE SHELF SÃO INSTANCIADOS JÁ COM OS NOVOS VALORES QUE ESTAVAM NA ORDEM DE COMPRAS.

        
        # order_number,
        # user_id,
        # total_order_price,
        # product_id,
        # product_unit_price,
        # product_total_price,
        # reserved_volume,
        # created_time,
        # expires_time

        # :order_number,:user_id,:total_order_price,:product_id,:product_unit_price,:product_total_price,:product_volume,:created_time,:expires_time

        # self.order_number = None
        # self.user_id = header["user_id"]
        # self.total_order_price = None
        # self.product_id_list = products["items"]
        # self.product_total_price = []
        # self.product_unit_price = []
        # self.created_time = None
        # self.expires_time = None

sample_payload = {
            "header": { 
                "correlation_id": "req_8f3a9b1c-2026",
                "client_type": "totem",
                "client_id": "TOTEM_LOJA_01",
                "user_id": "3",
                "role": "employee", #consumer, employee, manager
                "auth_token": "bearer.jwt.token.here",
                "action": "ORDER_CREATE",
                "timestamp": "1785816136"
            },
            "payload": {
                "items": [ #ITEMS COM S, NO PLURAL, POIS É LISTA DE ITENS
                    {
                        "product_id": 29,
                        "requested_volume": 3,
                    }
                ],
            }
    }