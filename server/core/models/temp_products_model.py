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
    def __init__(self,item: dict):
        self.product_name = item["product_name"]
        self.bar_code = item["bar_code"]
        self.price = item["price"]
        self.product_batch = item["product_batch"]
        self.validity = item["validity"]
        self.product_weight = item["product_weight"]
        self.shelf_id = item["shelf_id"]
        self.product_volume = item["product_volume"]

class RegisteredProduct:
    def __init__(self,bar_code: int, product_name: str, price: float, product_batch: str, validity: str, product_weight: float, shelf_id: int, product_volume: int):
        self.product_id = id
        self.bar_code = bar_code
        self.product_name = product_name
        self.price = price
        self.product_batch = product_batch
        self.validity = validity
        self.product_weight = product_weight
        self.shelf_id = shelf_id
        self.product_volume = product_volume
        self.reserved_volume = reserved_volume
        self.available = available