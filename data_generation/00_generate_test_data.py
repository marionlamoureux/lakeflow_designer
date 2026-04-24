# Databricks notebook source
# MAGIC %md
# MAGIC # Lakeflow Designer Lab - Test Data Generation
# MAGIC
# MAGIC **Scenario:** OTC Derivatives reporting for regulatory compliance (Finrep-inspired).
# MAGIC
# MAGIC This notebook creates interrelated tables in Unity Catalog plus an **Excel file** simulating
# MAGIC an ad-hoc business adjustment -- the exact pattern that needs industrializing.
# MAGIC
# MAGIC **Tables created (in Unity Catalog):**
# MAGIC - `counterparties` (200 rows) - Banks, corporates, funds
# MAGIC - `otc_trades` (10,000 rows) - OTC derivative trades (IRS, CDS, FX Fwd, Options)
# MAGIC - `settlements` (9,500 rows) - Settlement records (some trades have no settlement = breaks)
# MAGIC - `market_data` (1,200 rows) - Daily risk factors (rates, spreads, FX)
# MAGIC
# MAGIC **Excel file (drag-and-drop in Designer):**
# MAGIC - `regulatory_adjustments.xlsx` - Manual adjustments from the business team (the ECB pain point)
# MAGIC
# MAGIC **Usage:** Set the catalog and schema below, then Run All.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

CATALOG = "lab_lakeflow"
SCHEMA = "cft"

spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print(f"Using {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate Data

# COMMAND ----------

import random
from datetime import datetime, timedelta
from pyspark.sql import Row

random.seed(42)

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_ts(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

DATE_START = datetime(2024, 1, 1)
DATE_END = datetime(2026, 4, 20)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Counterparties

# COMMAND ----------

cpty_types = ["Bank", "Corporate", "Hedge Fund", "Asset Manager", "Insurance", "Central Counterparty"]
cpty_type_weights = [0.30, 0.25, 0.15, 0.15, 0.10, 0.05]
countries = ["FR", "DE", "GB", "US", "CH", "IT", "ES", "NL", "JP", "SG", "LU", "BE", "IE"]
ratings = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "NR"]
rating_weights = [0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.12, 0.10, 0.08, 0.06, 0.04, 0.03, 0.05]
sectors = ["Financial Services", "Energy", "Industrials", "Technology", "Healthcare", "Real Estate", "Utilities", "Consumer"]

bank_names = ["BNP Paribas", "Credit Agricole", "Deutsche Bank", "HSBC", "Barclays",
              "UBS", "Credit Suisse", "JPMorgan", "Goldman Sachs", "Morgan Stanley",
              "Natixis", "Commerzbank", "ING", "ABN AMRO", "Santander",
              "UniCredit", "Intesa Sanpaolo", "Nomura", "DBS", "Standard Chartered"]
corp_names = ["TotalEnergies", "Siemens", "AstraZeneca", "SAP", "LVMH",
              "Airbus", "Alstom", "Schneider Electric", "Engie", "Danone",
              "Sanofi", "L'Oreal", "Michelin", "Renault", "Thales",
              "Veolia", "Vinci", "Orange", "Pernod Ricard", "Hermes"]
fund_names = [f"Alpha Fund {i}" for i in range(1, 21)] + [f"Global Macro {i}" for i in range(1, 11)]

counterparties = []
for i in range(1, 201):
    ctype = random.choices(cpty_types, weights=cpty_type_weights, k=1)[0]
    if ctype == "Bank":
        name = random.choice(bank_names) if i <= 20 else f"Regional Bank {i}"
    elif ctype == "Corporate":
        name = random.choice(corp_names) if i <= 40 else f"Corp Entity {i}"
    else:
        name = random.choice(fund_names) if i <= 60 else f"{ctype} {i}"

    lei = f"LEI{i:04d}{random.choice(countries)}{random.randint(100000, 999999)}"
    country = random.choice(countries)
    rating = random.choices(ratings, weights=rating_weights, k=1)[0]
    sector = "Financial Services" if ctype in ["Bank", "Hedge Fund", "Asset Manager", "Insurance", "Central Counterparty"] else random.choice(sectors)
    netting_agreement = random.random() > 0.15
    csa_agreement = random.random() > 0.25

    counterparties.append(Row(
        counterparty_id=f"CPT-{i:04d}",
        counterparty_name=name,
        lei_code=lei,
        counterparty_type=ctype,
        country=country,
        credit_rating=rating,
        sector=sector,
        has_netting_agreement=netting_agreement,
        has_csa=csa_agreement,
        onboarding_date=random_date(datetime(2018, 1, 1), datetime(2025, 6, 1)).date()
    ))

df_counterparties = spark.createDataFrame(counterparties)
df_counterparties.write.mode("overwrite").saveAsTable("counterparties")
print(f"counterparties: {df_counterparties.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### OTC Trades

# COMMAND ----------

product_types = ["IRS", "CDS", "FX Forward", "FX Option", "Equity Option", "Commodity Swap", "Cross-Currency Swap"]
product_weights = [0.30, 0.20, 0.20, 0.10, 0.08, 0.07, 0.05]
currencies = ["EUR", "USD", "GBP", "CHF", "JPY", "SEK", "NOK"]
buy_sell = ["Buy", "Sell"]
books = ["FLOW-IRD", "FLOW-FX", "FLOW-CREDIT", "EXOTIC-EQ", "EXOTIC-COMM", "HEDGING", "CVA-DESK", "XVA-DESK"]
statuses = ["Live", "Matured", "Terminated", "Novated"]
status_weights = [0.60, 0.20, 0.12, 0.08]
clearing_types = ["Bilateral", "CCP-Cleared"]
clearing_weights = [0.45, 0.55]

cpty_ids = [f"CPT-{i:04d}" for i in range(1, 201)]

trades = []
for i in range(1, 10001):
    product = random.choices(product_types, weights=product_weights, k=1)[0]
    trade_date = random_date(DATE_START, DATE_END)
    tenor_days = random.choice([30, 60, 90, 180, 365, 730, 1095, 1825, 3650])
    maturity = trade_date + timedelta(days=tenor_days)
    ccy = random.choice(currencies)
    notional = round(random.choice([1, 2, 5, 10, 25, 50, 100]) * 1_000_000, 0)
    mtm = round(random.gauss(0, notional * 0.03), 2)
    status = random.choices(statuses, weights=status_weights, k=1)[0]
    clearing = random.choices(clearing_types, weights=clearing_weights, k=1)[0]

    trades.append(Row(
        trade_id=f"TRD-{i:06d}",
        counterparty_id=random.choice(cpty_ids),
        product_type=product,
        book=random.choice(books),
        trade_date=trade_date.date(),
        maturity_date=maturity.date(),
        notional_amount=notional,
        currency=ccy,
        direction=random.choice(buy_sell),
        mtm_eur=mtm,
        status=status,
        clearing_type=clearing,
        uti=f"UTI{random.randint(10**15, 10**16-1)}",
        trade_timestamp=random_ts(trade_date, trade_date + timedelta(hours=10))
    ))

df_trades = spark.createDataFrame(trades)
df_trades.write.mode("overwrite").saveAsTable("otc_trades")
print(f"otc_trades: {df_trades.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Settlements
# MAGIC
# MAGIC Some trades deliberately have NO settlement record (= breaks to detect in the lab).

# COMMAND ----------

settlement_statuses = ["Settled", "Pending", "Failed", "Partially Settled"]
settlement_weights = [0.70, 0.15, 0.10, 0.05]

trade_ids_all = [f"TRD-{i:06d}" for i in range(1, 10001)]
# ~5% of trades will have NO settlement (= breaks)
trade_ids_with_settlement = random.sample(trade_ids_all, 9500)

settlements = []
for idx, tid in enumerate(trade_ids_with_settlement):
    trade_num = int(tid.split("-")[1])
    trade_date = DATE_START + timedelta(days=(trade_num * 83) % (DATE_END - DATE_START).days)
    settle_date = trade_date + timedelta(days=random.choice([1, 2, 3, 5, 7]))
    sett_status = random.choices(settlement_statuses, weights=settlement_weights, k=1)[0]

    expected_amount = round(random.uniform(10_000, 50_000_000), 2)
    # Introduce some amount mismatches for "partial" breaks
    if sett_status == "Partially Settled":
        actual_amount = round(expected_amount * random.uniform(0.5, 0.95), 2)
    elif sett_status == "Failed":
        actual_amount = 0.0
    else:
        actual_amount = expected_amount if random.random() > 0.03 else round(expected_amount * random.uniform(0.98, 1.02), 2)

    ccy = random.choice(currencies)

    settlements.append(Row(
        settlement_id=f"STL-{idx+1:06d}",
        trade_id=tid,
        settlement_date=settle_date.date(),
        expected_amount=expected_amount,
        actual_amount=actual_amount,
        currency=ccy,
        settlement_status=sett_status,
        nostro_account=f"NOSTRO-{random.choice(currencies)}-{random.randint(1,5):02d}",
        settlement_method=random.choice(["SWIFT", "TARGET2", "CLS", "Internal"])
    ))

df_settlements = spark.createDataFrame(settlements)
df_settlements.write.mode("overwrite").saveAsTable("settlements")
print(f"settlements: {df_settlements.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Market Data (daily risk factors)

# COMMAND ----------

risk_factors = [
    ("EUR_SWAP_1Y", "Interest Rate", "EUR"), ("EUR_SWAP_5Y", "Interest Rate", "EUR"),
    ("EUR_SWAP_10Y", "Interest Rate", "EUR"), ("EUR_SWAP_30Y", "Interest Rate", "EUR"),
    ("USD_SWAP_1Y", "Interest Rate", "USD"), ("USD_SWAP_5Y", "Interest Rate", "USD"),
    ("USD_SWAP_10Y", "Interest Rate", "USD"), ("GBP_SWAP_5Y", "Interest Rate", "GBP"),
    ("EURUSD", "FX Rate", "USD"), ("EURGBP", "FX Rate", "GBP"),
    ("EURJPY", "FX Rate", "JPY"), ("EURCHF", "FX Rate", "CHF"),
    ("ITRAXX_MAIN_5Y", "Credit Spread", "EUR"), ("CDX_IG_5Y", "Credit Spread", "USD"),
    ("ITRAXX_XOVER_5Y", "Credit Spread", "EUR"),
    ("EUROSTOXX50", "Equity Index", "EUR"), ("SPX", "Equity Index", "USD"),
    ("BRENT_1M", "Commodity", "USD"), ("GOLD_SPOT", "Commodity", "USD"),
    ("EUR_VOL_3M", "Volatility", "EUR"),
]

base_values = {
    "EUR_SWAP_1Y": 3.2, "EUR_SWAP_5Y": 2.8, "EUR_SWAP_10Y": 2.9, "EUR_SWAP_30Y": 3.1,
    "USD_SWAP_1Y": 4.5, "USD_SWAP_5Y": 4.0, "USD_SWAP_10Y": 4.1, "GBP_SWAP_5Y": 3.8,
    "EURUSD": 1.08, "EURGBP": 0.86, "EURJPY": 162.5, "EURCHF": 0.95,
    "ITRAXX_MAIN_5Y": 65.0, "CDX_IG_5Y": 55.0, "ITRAXX_XOVER_5Y": 320.0,
    "EUROSTOXX50": 4800.0, "SPX": 5200.0, "BRENT_1M": 82.0, "GOLD_SPOT": 2350.0,
    "EUR_VOL_3M": 12.5,
}

market_data = []
# Generate for a few reporting dates
reporting_dates = [datetime(2026, 3, 31), datetime(2026, 2, 28), datetime(2026, 1, 31), datetime(2025, 12, 31)]

for report_date in reporting_dates:
    for rf_name, rf_type, rf_ccy in risk_factors:
        base = base_values[rf_name]
        # Add some random walk
        value = round(base * (1 + random.gauss(0, 0.02)), 6)
        prev_value = round(base * (1 + random.gauss(0, 0.02)), 6)
        market_data.append(Row(
            risk_factor=rf_name,
            risk_factor_type=rf_type,
            currency=rf_ccy,
            reporting_date=report_date.date(),
            value=value,
            previous_value=prev_value,
            change_pct=round((value - prev_value) / prev_value * 100, 4),
            source="Reuters"
        ))

df_market = spark.createDataFrame(market_data)
df_market.write.mode("overwrite").saveAsTable("market_data")
print(f"market_data: {df_market.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Excel file: Regulatory Adjustments
# MAGIC
# MAGIC This simulates the ad-hoc business input that ECB requires to industrialize.
# MAGIC Business teams send manual adjustments as Excel files -- this is exactly the pattern
# MAGIC that Lakeflow Designer needs to handle (drag-and-drop Excel onto the canvas).

# COMMAND ----------

import pandas as pd

spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.lab_files")

# Sheet 1: Manual MTM adjustments from the business
adjustments = []
for i in range(1, 31):
    tid = f"TRD-{random.randint(1, 10000):06d}"
    adj_type = random.choice(["MTM Override", "Notional Correction", "Maturity Extension", "Counterparty Reclassification", "Collateral Haircut"])
    adjustments.append({
        "adjustment_id": f"ADJ-{i:03d}",
        "trade_id": tid,
        "adjustment_type": adj_type,
        "original_value": round(random.uniform(-5_000_000, 5_000_000), 2),
        "adjusted_value": round(random.uniform(-5_000_000, 5_000_000), 2),
        "justification": random.choice([
            "ECB audit finding - Q1 2026",
            "Model recalibration",
            "Counterparty downgrade",
            "Netting set restructure",
            "CSA threshold update",
            "Manual correction per risk committee",
            "Regulatory capital floor adjustment"
        ]),
        "approved_by": random.choice(["P. Fitz", "C. Pernoud", "T. Rodary", "B. Pathsamatla", "O. Burg"]),
        "approval_date": str(random_date(datetime(2026, 3, 1), datetime(2026, 4, 20)).date()),
        "status": random.choice(["Approved", "Pending Review", "Approved"])
    })

df_adj = pd.DataFrame(adjustments)

# Sheet 2: Reporting thresholds per product type
thresholds = pd.DataFrame({
    "product_type": ["IRS", "CDS", "FX Forward", "FX Option", "Equity Option", "Commodity Swap", "Cross-Currency Swap"],
    "materiality_threshold_eur": [100_000, 250_000, 50_000, 150_000, 200_000, 300_000, 100_000],
    "reporting_frequency": ["Daily", "Daily", "Daily", "Weekly", "Weekly", "Monthly", "Daily"],
    "ecb_template_ref": ["F10.1a", "F10.1b", "F10.2a", "F10.2b", "F10.3", "F10.4", "F10.1c"]
})

# Write as Excel with 2 sheets
volume_path = f"/Volumes/{CATALOG}/{SCHEMA}/lab_files"
excel_path = f"{volume_path}/regulatory_adjustments.xlsx"

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_adj.to_excel(writer, sheet_name="Adjustments", index=False)
    thresholds.to_excel(writer, sheet_name="Thresholds", index=False)

print(f"regulatory_adjustments.xlsx written to Volume ({len(df_adj)} adjustments, {len(thresholds)} thresholds)")

# Also save as CSV for alternative import
df_adj.to_csv(f"{volume_path}/regulatory_adjustments.csv", index=False)
print("regulatory_adjustments.csv also written (backup)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify

# COMMAND ----------

for table in ["counterparties", "otc_trades", "settlements", "market_data"]:
    count = spark.table(table).count()
    print(f"  {CATALOG}.{SCHEMA}.{table}: {count:,} rows")

print(f"\nExcel file: {excel_path}")
print("\nAll tables ready. Open Lakeflow Designer and start the lab!")
print("Remember: drag-and-drop the Excel file from the Volume onto the Designer canvas.")
