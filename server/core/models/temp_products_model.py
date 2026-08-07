class Product:
    def __init__(self,bar_code: int, product_name: str, price: float, product_batch: str, validity: str, product_weight: float, cabinet_shelf_id: int, product_volume: int):
        self.bar_code = bar_code
        self.product_name = product_name
        self.price = price
        self.product_batch = product_batch
        self.validity = validity
        self.product_weight = product_weight
        self.cabinet_shelf_id = cabinet_shelf_id
        self.product_volume = product_volume