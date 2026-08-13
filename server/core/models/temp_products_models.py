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