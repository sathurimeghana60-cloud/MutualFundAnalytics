PRAGMA foreign_keys = ON;

-- =========================
-- Dimension: Fund
-- =========================
CREATE TABLE IF NOT EXISTS dim_fund (
    fund_key INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER UNIQUE NOT NULL,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

-- =========================
-- Dimension: Date
-- =========================
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    year INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER
);

-- =========================
-- Fact: NAV
-- =========================
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_key INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    nav REAL NOT NULL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

-- =========================
-- Fact: Transactions
-- =========================
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_key INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_key INTEGER,
    transaction_type TEXT,
    amount REAL,
    state TEXT,
    kyc_status TEXT,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

-- =========================
-- Fact: Performance
-- =========================
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_key INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_key INTEGER,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    expense_ratio REAL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

-- =========================
-- Fact: AUM
-- =========================
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_key INTEGER PRIMARY KEY AUTOINCREMENT,
    date_key INTEGER,
    fund_house TEXT,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);