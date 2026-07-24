import threading
import queue

from server.core.controllers import product_controller as prod_ctrl

event_type_queue = queue.Queue()


class ProductActions:
    def __init__(self):
        self.event_mapping = {
            "ADD_NEW_PRODUCT": prod_ctrl.new_product,
            "EDIT_PRODUCT": prod_ctrl.change_product_info,
            "SEARCH_PRODUCT": prod_ctrl.search_product_name,
            "LIST_ALL_PRODUCTS": prod_ctrl.list_all_products,
        }

    def inventory_proccess(self):
        while True:
            event_package = event_type_queue.get()

            try:
                event_type = event_package.get("eventType",)

                if not event_type:
                    print(f"\n[BANCO DE DADOS - INVENTÁRIO] COMANDO INVÁLIDO.\n")
                    continue

                event_comand = self.event_mapping.get(event_type,)

                if not event_comand:
                    print(f"\n[BANCO DE DADOS - INVENTÁRIO] COMANDO INVÁLIDO.\n")
                    continue
                
                args = event_package.get("args",[])

                if not isinstance(args, (list, tuple)):
                    args = [args] if args is not None else []

                
                event_comand(*args)

            except Exception as error:
                print(f"\n[BANCO DE DADOS - INVENTÁRIO] ERRO NA SOLICITAÇÃO: [{error}].\n")

            finally:
                event_type_queue.task_done()