from datetime import datetime, timedelta

class LockManagment:
    def __init__(self):
        self.token_dict = {}
        self.lock_status = "locked" #SIMULATES IF DOOR IS LOCKED OR UNLOCKED

    def insert_token_dict(self,order_token:str):
        time_now = datetime.now()
        expires_token_time = time_now + timedelta(minutes=10)
        token_dict[order_token] = {"expires_token_time":expires_token_time, "lock_status":"unlock"}
    
    def unlock_door(self,order_token:str):
        time_now = datetime.now()
        if order_token in self.token_dict:
            lock_status = self.token_dict[order_token]["lock_status"]
            expires_token_time = self.token_dict[order_token]["expires_token_time"]

            if lock_status == "unlock" and expires_token_time > time_now:
                self.lock_status = "unlocked"
                print("\n[ARMÁRIO INTELIGENTE] PORTA ABERTA. POR FAVOR, RETIRE SEUS PRODUTOS.\n")
            else:
                print("\n[ARMÁRIO INTELIGENTE] TOKEN COM PRAZO DE TEMPO EXPIRADO. SOLICITE NOVO TOKEN.\n")
        else:
            print("\n[ARMÁRIO INTELIGENTE] TOKEN INVÁLIDO. DIGITE NOVAMENTE O TOKEN.\n")