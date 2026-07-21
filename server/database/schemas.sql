-- Script puramente DDL (Criação de tabelas, índices e triggers)
-- REMEMBER: LEARN ABOUT INDEX FOR GET THE EXACT ID LINE FOR MOST SELECTED DATA
PRAGMA foreign_keys = On;

-- 1.Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    document TEXT UNIQUE NOT NULL,
    type_user TEXT NOT NULL CHECK (type_user IN('CLIENTE','GERENTE','COLABORADOR')),
    created_time DATETIME DEFAULT CURRENT_DATE,
    blocked_until DATETIME NULL,
    consecutive_cancel INTEGER DEFAULT 0
);


-- 2.Products and locations table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unique_code INTEGER UNIQUE NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL CHECK (price > 0),
    validity DATE NOT NULL,
    weight_gram_unit REAL NOT NULL CHECK (weight_gram_unit > 0),
    cabinet_id INTEGER NOT NULL,
    cabinet_shelf_id INTEGER NOT NULL, -- is the weight scale itselfs
    total_inventory_amount INTEGER NOT NULL CHECK (total_inventory_amount >= 0),
    reserved_inventory_amount INTEGER DEFAULT 0 CHECK(reserved_inventory_amount >= 0)
);


-- 3.Reservation table (mobile app)
CREATE TABLE IF NOT EXISTS reservation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    amount_reserved INTEGER NOT NULL CHECK (amount_reserved > 0),
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_time DATETIME NOT NULL,
    reserve_status TEXT DEFAULT 'PENDENTE' CHECK (reserve_status IN ('PENDENTE', 'CONCLUIDA', 'EXPIRADA', 'CANCELADA')),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 4.Order table (withdrawal and token session)
CREATE TABLE IF NOT EXISTS order_kart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL, -- 4 digits code (eg.:4829)
    total_price REAL NOT NULL,
    plataform_order TEXT NOT NULL CHECK (plataform_order IN ('TOTEM_PDV', 'APP_MOBILE')),
    order_status TEXT DEFAULT 'PENDENTE' CHECK (order_status IN ('PENDENTE', 'EM_COLETA', 'CONCLUIDO', 'CANCELADO')),
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 5.Order items table (rel order x purchased)
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    amount_items INTEGER NOT NULL CHECK (amount_items > 0),
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES order_kart(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 6.Withdrawal weight audit table (scale register per cabinet shelf)
CREATE TABLE IF NOT EXISTS withdrawal_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    cabinet_shelf_id INTEGER NOT NULL, -- id from the current scale
    previous_weight_grams REAL NULL,
    current_weight_grams REAL NULL,
    expected_weight_grams REAL NOT NULL,
    weight_status TEXT DEFAULT 'PENDENTE' CHECK (weight_status IN ('PENDENTE', 'SUCESSO', 'DIVERGENTE')),
    withdrawal_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES order_kart(id)
);