class NewProduct:
    sample_payload = {
            "header": { 
                "correlation_id": "req_8f3a9b1c-2026",
                "client_type": "totem",
                "client_id": "TOTEM_LOJA_01",
                "user_id": "3",
                "role": "employee", #consumer, employee, manager
                "auth_token": "bearer.jwt.token.here",
                "action": "NEW_PRODUCT",
                "timestamp": "1785816136"
            },
            "payload": {
                "item": {
                    "product_name": "New Product",
                    "bar_code": "199999999",
                    "price": 10.99,
                    "product_batch": "BATCH_001",
                    "validity": "2023-12-31",
                    "product_weight": 1.5,
                    "shelf_id": 1,
                    "product_volume": 2.0
                }
            }
        }
    def __init__(self,product: dict):
        self.product_name = product["product_name"]
        self.bar_code = product["bar_code"]
        self.price = product["price"]
        self.product_batch = product["product_batch"]
        self.validity = product["validity"]
        self.product_weight = product["product_weight"]
        self.shelf_id = product["shelf_id"]
        self.product_volume = product["product_volume"]

class RealStockProduct:
    def __init__(self,product: dict):
        self.product_id = product["product_id"]
        self.bar_code = product["bar_code"]
        self.product_name = product["product_name"]
        self.price = product["price"]
        self.product_batch = product["product_batch"]
        self.validity = product["validity"]
        self.product_weight = product["product_weight"]
        self.shelf_id = product["shelf_id"]
        self.product_volume = product["product_volume"]
        self.available = product["available"]

class ReservedProduct:
    def __init__(self,product: dict):
        self.product_id = product["product_id"]
        self.reserved_volume = product["reserved_volume"]
    
class OrderProduct:
    def __init__(self,product: dict):
        self.product_id = product["product_id"]
        self.requested_volume = product["requested_volume"]

class PurchaseOrder:
    def __init__(self,header: dict, products: dict): #VERIFICAR A NECESSIDADE DE INSERIR O OBJETO DA CONEXAO
        self.order_number: int | None = None
        self.user_id = header["user_id"]
        self.total_order_price: float | None = None
        self.product_id_list = products["items"]
        self.product_total_price = []
        self.product_unit_price = []
        self.weight_to_reduce = []
        self.volume_to_reduce = []
        self.created_time: str | None =None
        self.expires_time: str | None = None
        self.reserve_status = "PENDENTE"
        self.payment_status = "PENDENTE"
