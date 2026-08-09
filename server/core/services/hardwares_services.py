class HardwareServices:
    def __init__(self):
        



sample_payload = {
    "header":
    {
        "correlation_id": "req_8f3a9b1c-2026",
        "client_type": "totem",
        "client_id": "TOTEM_LOJA_01",
        "user_id": "3",
        "role": "employee", #consumer, employee, manager
        "auth_token": "bearer.jwt.token.here",
        "action": "INSTALL_NEW_CABINET", #INSTALL_NEW_CABINET, GET_CABINET_INFO, INSTALL_NEW_SHELF, GET_SHELF_INFO
        "timestamp": "1785816136"
    },
    "payload":
    {
        "hardware_mac_address": "xx:xx:xx:xx:xx",
        "hardware_tcp_port": "80001",
        "hardware_current_ip_address": "192.168.1.245"
    },
}