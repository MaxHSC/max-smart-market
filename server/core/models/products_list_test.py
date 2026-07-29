products_list = [
    # --- PRODUTO EM 3 PRATELEIRAS (2 com mesmo lote, 1 com lote diferente) ---
    {
        "bar_code": 7891000000011,
        "product_name": "Arroz Agulhinha 1kg",
        "price": 5.99,
        "product_batch": "LOTE-ARR-2026A",
        "validity": "2026-12-31",
        "product_weight": 1.0,
        "cabinet_shelf_id": 1,
        "product_volume": 10,
    },
    {
        
        "bar_code": 7891000000011,
        "product_name": "Arroz Agulhinha 1kg",
        "price": 5.99,
        "product_batch": "LOTE-ARR-2026A",  # Mesmo lote/validade da prateleira 1
        "validity": "2026-12-31",
        "product_weight": 1.0,
        "cabinet_shelf_id": 2,
        "product_volume": 8,
    },
    {
        "bar_code": 7891000000011,
        "product_name": "Arroz Agulhinha 1kg",
        "price": 6.20,
        "product_batch": "LOTE-ARR-2026B",  # Lote e validade diferentes
        "validity": "2027-02-28",
        "product_weight": 1.0,
        "cabinet_shelf_id": 3,
        "product_volume": 12,
    },
    # --- DEMAIS PRODUTOS DISTRIBUÍDOS NAS PRATELEIRAS ---
    {
        "bar_code": 7891000000028,
        "product_name": "Feijão Preto 1kg",
        "price": 8.50,
        "product_batch": "LOTE-FEI-101",
        "validity": "2026-10-15",
        "product_weight": 1.0,
        "cabinet_shelf_id": 1,  # Prateleira 1 total: 10 + 6 = 16 un | 16kg
        "product_volume": 6,
    },
    {
        "bar_code": 7891000000035,
        "product_name": "Açúcar Refinado 1kg",
        "price": 4.30,
        "product_batch": "LOTE-ACU-002",
        "validity": "2027-05-20",
        "product_weight": 1.0,
        "cabinet_shelf_id": 2,  # Prateleira 2 total: 8 + 10 = 18 un | 18kg
        "product_volume": 10,
    },
    {
        "bar_code": 7891000000042,
        "product_name": "Café Torrado 500g",
        "price": 16.90,
        "product_batch": "LOTE-CAF-99",
        "validity": "2026-09-30",
        "product_weight": 0.5,
        "cabinet_shelf_id": 3,  # Prateleira 3 total: 12 + 8 = 20 un | 16kg
        "product_volume": 8,
    },
    {
        "bar_code": 7891000000059,
        "product_name": "Óleo de Soja 900ml",
        "price": 7.49,
        "product_batch": "LOTE-OLE-44",
        "validity": "2026-11-10",
        "product_weight": 0.9,
        "cabinet_shelf_id": 4,  # Prateleira 4 total: 15 un | 13.5kg
        "product_volume": 15,
    },
    {
        "bar_code": 7891000000066,
        "product_name": "Leite Integral 1L",
        "price": 5.29,
        "product_batch": "LOTE-LEI-12",
        "validity": "2026-08-01",
        "product_weight": 1.03,
        "cabinet_shelf_id": 5,  # Prateleira 5 total: 14 un | 14.42kg
        "product_volume": 14,
    },
    {
        "bar_code": 7891000000073,
        "product_name": "Macarrão Espaguete 500g",
        "price": 3.99,
        "product_batch": "LOTE-MAC-88",
        "validity": "2027-01-15",
        "product_weight": 0.5,
        "cabinet_shelf_id": 6,  # Prateleira 6 total: 20 un | 10kg
        "product_volume": 20,
    },
    {
        "bar_code": 7891000000080,
        "product_name": "Sal Refinado 1kg",
        "price": 2.50,
        "product_batch": "LOTE-SAL-01",
        "validity": "2028-01-01",
        "product_weight": 1.0,
        "cabinet_shelf_id": 7,  # Prateleira 7 total: 12 un | 12kg
        "product_volume": 12,
    },
    {
        "bar_code": 7891000000097,
        "product_name": "Farinha de Trigo 1kg",
        "price": 4.89,
        "product_batch": "LOTE-FAR-55",
        "validity": "2026-12-10",
        "product_weight": 1.0,
        "cabinet_shelf_id": 8,  # Prateleira 8 total: 15 un | 15kg
        "product_volume": 15,
    },
    {
        "bar_code": 7891000000103,
        "product_name": "Detergente Líquido 500ml",
        "price": 2.29,
        "product_batch": "LOTE-DET-301",
        "validity": "2027-06-30",
        "product_weight": 0.5,
        "cabinet_shelf_id": 9,  # Prateleira 9 total: 18 un | 9kg
        "product_volume": 18,
    },
    {
        "bar_code": 7891000000110,
        "product_name": "Sabão em Pó 1kg",
        "price": 12.90,
        "product_batch": "LOTE-SAB-09",
        "validity": "2027-08-15",
        "product_weight": 1.0,
        "cabinet_shelf_id": 10,  # Prateleira 10 total: 10 un | 10kg
        "product_volume": 10,
    },
    {
        "bar_code": 7891000000127,
        "product_name": "Desinfetante 1L",
        "price": 6.79,
        "product_batch": "LOTE-DES-77",
        "validity": "2027-04-12",
        "product_weight": 1.0,
        "cabinet_shelf_id": 11,  # Prateleira 11 total: 12 un | 12kg
        "product_volume": 12,
    },
    {
        "bar_code": 7891000000134,
        "product_name": "Achocolatado 400g",
        "price": 7.99,
        "product_batch": "LOTE-ACH-14",
        "validity": "2026-11-30",
        "product_weight": 0.4,
        "cabinet_shelf_id": 12,  # Prateleira 12 total: 16 un | 6.4kg
        "product_volume": 16,
    },
    {
        "bar_code": 7891000000141,
        "product_name": "Biscoito Recheado 140g",
        "price": 2.99,
        "product_batch": "LOTE-BIS-03",
        "validity": "2026-09-15",
        "product_weight": 0.14,
        "cabinet_shelf_id": 13,  # Prateleira 13 total: 20 un | 2.8kg
        "product_volume": 20,
    },
    {
        "bar_code": 7891000000158,
        "product_name": "Sardinha em Lata 125g",
        "price": 4.50,
        "product_batch": "LOTE-SAR-88",
        "validity": "2028-03-20",
        "product_weight": 0.125,
        "cabinet_shelf_id": 14,  # Prateleira 14 total: 15 un | 1.875kg
        "product_volume": 15,
    },
    {
        "bar_code": 7891000000165,
        "product_name": "Molho de Tomate 340g",
        "price": 2.89,
        "product_batch": "LOTE-MOL-40",
        "validity": "2026-10-10",
        "product_weight": 0.34,
        "cabinet_shelf_id": 4,  # Adicionado à Prateleira 4 (+3 un | +1.02kg -> total 18 un, 14.52kg)
        "product_volume": 3,
    },
    {
        "bar_code": 7891000000172,
        "product_name": "Papel Toalha 2 un",
        "price": 5.49,
        "product_batch": "LOTE-PAP-01",
        "validity": "2029-01-01",
        "product_weight": 0.2,
        "cabinet_shelf_id": 5,  # Adicionado à Prateleira 5 (+5 un | +1.0kg -> total 19 un, 15.42kg)
        "product_volume": 5,
    },
    {
        "bar_code": 7891000000189,
        "product_name": "Milho em Conserva 170g",
        "price": 3.20,
        "product_batch": "LOTE-MIL-22",
        "validity": "2027-07-04",
        "product_weight": 0.17,
        "cabinet_shelf_id": 10,  # Adicionado à Prateleira 10 (+8 un | +1.36kg -> total 18 un, 11.36kg)
        "product_volume": 8,
    }
]