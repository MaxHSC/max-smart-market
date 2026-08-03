from datetime import datetime, timedelta
import random
import struct


def generate_token() -> tuple:
    random_number = random.randint(111111,999999)
    expires_token = datetime.now() + timedelta(minutes=10)

    return random_number, expires_token

def mount_token_payload(order_token: str, expires_token: datetime, cabinet_id_list: list):
    order_token_byte = order_token.encode("uft-8")
    expires_token_byte = expires_token.strftime("%Y-%m-%d %H:%M:%S").encode("utf-8")
    palyoad_size = len(order_token_byte + expires_token_byte)
    header = struct.pack('>I',payload_size)

    payload_package = header + order_token_byte + expires_token_byte

    return payload_package