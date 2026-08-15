from server.database import inventory_dao as inv_dao, hardware_dao as hard_dao
from server.core.models import temp_products_models as prod_mod
from server.core.models import temp_hardware_models as hard_mod
from server.core.validators import shopping_validators as serv_val

class ShoppingServices:
    def __init__(self):
        self.action_mapping = {
            "ORDER_CREATE": self.reserve_order,
            "ORDER_CANCEL": cancel_order_validation,
            "ORDER_RESTORE": restore_order_validation,
            "ORDER_CONCLUDE": conclude_order_validation,
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
        product_info: dict = inv_dao.get_product_real_stock_info(body_payload)

        if product_info is None:
            return None
        
        real_stock_product_object: prod_mod.RealStockProduct = prod_mod.RealStockProduct(product_info)

        return real_stock_product_object
    
    def get_product_reserved_stock_object(self, header: dict, body_payload: dict) -> prod_mod.ReservedProduct | None:
        product_info: dict = inv_dao.get_product_reserved_stock_info(body_payload)

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


    def reserve_order(self,header:dict,body_payload:dict):
        item_list: list[dict] = body_payload["items"]
        real_stock_products_object_list = []
        reserved_products_object_list = []
        order_products_list = []
        shelfs_object_list = []
        shelf_mapping = {}

        for product in item_list:
            real_product_object: prod_mod.RealStockProduct = self.get_product_real_stock_object(header,product)
            real_stock_products_object_list.append(real_product_object)

            reserved_product_object = self.get_product_reserved_stock_object(header,product)
            if reserved_product_object is not None:
                reserved_products_object_list.append(reserved_product_object)
            
            order_product_object: prod_mod.OrderProduct = prod_mod.OrderProduct(product)
            order_products_list.append(order_product_object)
        

        reserved_products_mapping = {reserved_object.id: reserved_object.reserved_volume for reserved_object in reserved_products_object_list}

        real_stock_products_mapping = {real_object.id: real_object for real_object in real_stock_products_object_list}

        for order_product in order_products_list:
            real_object = real_stock_products_mapping.get(order_product.id)

            reserved_volume = 0

            if real_object:
                reserved_volume = reserved_products_object_list.get((order_product.id), 0)
            
            avaliable_volume = real_object.product_volume - reserved_volume

            if avaliable_volume < order_product.requested_volume:
                return False
        

        for order_product in order_products_list:
            real_object = real_stock_products_mapping.get(order_product.id)

            shelf_id_dict = {"shelf_id":real_object.shelf_id}

            shelf_object = self.get_shelf_object(shelf_id_dict)
            shelfs_object_list.append(shelf_object)

            if shelf_object.id not in shelf_mapping:
                shelf_mapping[shelf_object.id] = shelf_object
            
            if shelf_object.current_volume - order_product.requested_volume > shelf_object.volume_capacity or shelf_object.current_volume - order_product.requested_volume < 0:
                return False
            
            if shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume) > shelf_object.weight_capacity_grams or shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume) < 0:
                return False
            
            shelf_object.current_volume = shelf_object.current_volume - order_product.requested_volume
            shelf_object.current_weight_grams = shelf_object.current_weight_grams - (real_object.product_weight * order_product.requested_volume)
    

        total_order_price = 0
        product_total_price = []
        product_unit_price = []
        for order_product in order_products_list:
            real_object = real_stock_products_mapping.get(order_product.id)

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
        

        order_number = inv_dao.get_last_order_number() + 1

        created_order_time = datetime.now() #NÃO É DECLARADO, ASSUME VALOR DEFAULT NO DB
        expires_order_time = created_order_time + timedelta(minutes=order[0]["expires_time"])
        created_order_time_str = created_order_time.strftime("%Y-%m-%d %H:%M:%S")
        expires_order_time_str = expires_order_time.strftime("%Y-%m-%d %H:%M:%S")

        order_object: prod_mod.PurchaseOrder = prod_mod.PurchaseOrder(header,body_payload)
        order_object.order_number = order_number
        order_object.total_order_price = total_order_price
        order_object.product_total_price = product_total_price
        order_object.product_unit_price = product_unit_price
        order_object.created_time = created_order_time_str
        order_object.expires_time = expires_order_time_str

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
        
        confirm_order_reservation: bool = inv_dao.reserve_order(order_list)

        if not confirm_order_reservation:
            return False
        
        return confirm_order_reservation


    def restore_order(self,header:dict,body_payload:dict):
        
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