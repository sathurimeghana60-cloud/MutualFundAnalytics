-- =========================================================
-- 1. TOP 5 FUNDS BY AUM
-- =========================================================

SELECT
    fund_house,
    aum_crore
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5;


-- =========================================================
-- 2. AVERAGE NAV PER MONTH
-- =========================================================

SELECT
    d.year,
    d.month,
    ROUND(AVG(n.nav), 2) AS average_nav
FROM fact_nav n
JOIN dim_date d
    ON n.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- =========================================================
-- 3. SIP YEAR-OVER-YEAR GROWTH
-- =========================================================

SELECT
    CAST(strftime('%Y', d.date) AS INTEGER) AS year,
    ROUND(SUM(s.amount_crore), 2) AS total_sip_inflow
FROM fact_sip_inflows s
JOIN dim_date d
    ON s.date_key = d.date_key
GROUP BY year
ORDER BY year;


-- =========================================================
-- 4. TRANSACTIONS BY STATE
-- =========================================================

SELECT
    state,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;


-- =========================================================
-- 5. FUNDS WITH EXPENSE RATIO < 1%
-- =========================================================

SELECT
    f.scheme_name,
    f.fund_house,
    p.expense_ratio_pct
FROM dim_fund f
JOIN fact_performance p
    ON f.amfi_code = p.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct;


-- =========================================================
-- 6. TOP 5 FUNDS BY 1-YEAR RETURN
-- =========================================================

SELECT
    f.scheme_name,
    f.fund_house,
    p.return_1yr_pct
FROM dim_fund f
JOIN fact_performance p
    ON f.amfi_code = p.amfi_code
ORDER BY p.return_1yr_pct DESC
LIMIT 5;


-- =========================================================
-- 7. TOTAL AUM BY FUND HOUSE
-- =========================================================

SELECT
    fund_house,
    ROUND(SUM(aum_crore), 2) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC;


-- =========================================================
-- 8. TRANSACTIONS BY TRANSACTION TYPE
-- =========================================================

SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;


-- =========================================================
-- 9. NUMBER OF FUNDS BY RISK CATEGORY
-- =========================================================

SELECT
    risk_category,
    COUNT(*) AS fund_count
FROM dim_fund
GROUP BY risk_category
ORDER BY fund_count DESC;


-- =========================================================
-- 10. HIGHEST NAV FUNDS
-- =========================================================

SELECT
    f.scheme_name,
    f.fund_house,
    MAX(n.nav) AS highest_nav
FROM fact_nav n
JOIN dim_fund f
    ON n.amfi_code = f.amfi_code
GROUP BY f.amfi_code, f.scheme_name, f.fund_house
ORDER BY highest_nav DESC
LIMIT 10;