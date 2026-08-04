# Abre a porta TCP e escuta conexões brutas
"""
===============================================================================
 ARQUITETURA DO SERVIDOR: EVENT LOOP (MULTIPLEXAÇÃO) + WORKER POOL
===============================================================================

1. CAMADA DE I/O (MULTIPLICAÇÃO COM SELECT):
   - Responsável por escutar portas, aceitar novas conexões e ler/escrever bytes.
   - Opera de forma NÃO-BLOQUEANTE em uma thread dedicada (Event Loop).
   - Gerencia 'File Descriptors' únicos mapeados pelo Kernel do SO.
   - Garante que a I/O da rede não trave o processamento de outros clientes.

2. CAMADA DE PROCESSAMENTO (WORKER POOL MANUAL):
   - Conjunto fixo de WorkerThreads reusáveis consumindo de uma 'queue.Queue'.
   - Desacopla a I/O da regra de negócio (validação, banco de dados, auth).
   - Impede o consumo descontrolado de memória RAM sob picos de acesso.

3. CICLO DE VIDA DA REQUISIÇÃO (TASK CONTEXT):
   - O Event Loop lê os bytes e encapsula no 'TaskContext' (Socket + Payload + Metadados).
   - O Worker extrai o contexto, processa a regra de negócio e responde no socket.
   - Socket envia com 'timeout' configurado para evitar gargalos por conexões lentas.
===============================================================================
"""

payload_sample ={
  "header": {
    "correlation_id": "req_8f3a9b1c-2026",
    "client_type": "totem",
    "client_id": "TOTEM_LOJA_01",
    "role": "consumer",
    "auth_token": "bearer.jwt.token.here",
    "action": "ORDER_CREATE",
    "timestamp": 1785816136
  },
  "payload": {
    "items": [
      { "product_id": 104, "quantity": 2 }
    ],
    "payment_method": "PIX"
  }
}