# Databricks notebook source
# MAGIC %md
# MAGIC # Lakeflow Designer Lab - Test Data Generation
# MAGIC
# MAGIC This notebook creates 6 interrelated tables in Unity Catalog for the Lakeflow Designer hands-on lab.
# MAGIC
# MAGIC **Tables created:**
# MAGIC - `customers` (5,000 rows)
# MAGIC - `products` (500 rows)
# MAGIC - `stores` (50 rows)
# MAGIC - `suppliers` (100 rows)
# MAGIC - `orders` (25,000 rows)
# MAGIC - `order_items` (75,000 rows)
# MAGIC
# MAGIC **Usage:** Set the catalog and schema below, then Run All.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

CATALOG = "lab_lakeflow"
SCHEMA = "retail"

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
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType,
    DateType, TimestampType, BooleanType, LongType
)

random.seed(42)

# ---------- helpers ----------
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
# MAGIC ### Customers

# COMMAND ----------

first_names_m = ["Lucas", "Hugo", "Louis", "Gabriel", "Arthur", "Nathan", "Jules", "Adam", "Raphael", "Leo",
                 "Paul", "Ethan", "Noel", "Tom", "Mathis", "Theo", "Sacha", "Maxime", "Antoine", "Alexandre"]
first_names_f = ["Emma", "Jade", "Louise", "Alice", "Chloe", "Lea", "Manon", "Rose", "Anna", "Lina",
                 "Camille", "Sarah", "Juliette", "Marie", "Clara", "Lucie", "Ines", "Eva", "Zoe", "Margaux"]
last_names = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau",
              "Simon", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier",
              "Morel", "Girard", "Andre", "Mercier", "Dupont", "Lambert", "Bonnet", "Francois", "Martinez", "Faure"]
cities = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille",
          "Rennes", "Reims", "Toulon", "Grenoble", "Dijon", "Angers", "Nimes", "Clermont-Ferrand", "Le Havre", "Aix-en-Provence"]
regions = {"Paris": "Ile-de-France", "Lyon": "Auvergne-Rhone-Alpes", "Marseille": "Provence-Alpes-Cote d'Azur",
           "Toulouse": "Occitanie", "Nice": "Provence-Alpes-Cote d'Azur", "Nantes": "Pays de la Loire",
           "Strasbourg": "Grand Est", "Montpellier": "Occitanie", "Bordeaux": "Nouvelle-Aquitaine", "Lille": "Hauts-de-France",
           "Rennes": "Bretagne", "Reims": "Grand Est", "Toulon": "Provence-Alpes-Cote d'Azur",
           "Grenoble": "Auvergne-Rhone-Alpes", "Dijon": "Bourgogne-Franche-Comte", "Angers": "Pays de la Loire",
           "Nimes": "Occitanie", "Clermont-Ferrand": "Auvergne-Rhone-Alpes", "Le Havre": "Normandie",
           "Aix-en-Provence": "Provence-Alpes-Cote d'Azur"}
loyalty_tiers = ["Bronze", "Silver", "Gold", "Platinum"]
loyalty_weights = [0.40, 0.30, 0.20, 0.10]

customers = []
for i in range(1, 5001):
    gender = random.choice(["M", "F"])
    fn = random.choice(first_names_m if gender == "M" else first_names_f)
    ln = random.choice(last_names)
    city = random.choice(cities)
    age = random.randint(18, 78)
    tier = random.choices(loyalty_tiers, weights=loyalty_weights, k=1)[0]
    signup = random_date(datetime(2020, 1, 1), DATE_END)
    email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
    active = random.random() > 0.08
    customers.append(Row(
        customer_id=i, first_name=fn, last_name=ln, email=email,
        gender=gender, age=age, city=city, region=regions[city],
        loyalty_tier=tier, signup_date=signup.date(), is_active=active
    ))

df_customers = spark.createDataFrame(customers)
df_customers.write.mode("overwrite").saveAsTable("customers")
print(f"customers: {df_customers.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Products

# COMMAND ----------

categories = {
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers", "Hoodie", "Shorts", "Sweater", "Coat", "Scarf"],
    "Electronics": ["Headphones", "Charger", "Tablet Case", "USB Hub", "Webcam", "Mouse", "Keyboard", "Speaker", "Power Bank", "Monitor Stand"],
    "Home": ["Candle", "Cushion", "Vase", "Throw Blanket", "Picture Frame", "Lamp", "Rug", "Clock", "Mirror", "Plant Pot"],
    "Beauty": ["Moisturizer", "Shampoo", "Lipstick", "Sunscreen", "Perfume", "Serum", "Nail Polish", "Conditioner", "Face Mask", "Body Lotion"],
    "Food": ["Coffee Beans", "Chocolate Bar", "Olive Oil", "Pasta", "Honey", "Tea", "Jam", "Biscuits", "Cereal", "Granola"]
}
brands = {
    "Apparel": ["Maison Mode", "Atelier Parisien", "Rue du Style"],
    "Electronics": ["TechNova", "PixelWave", "ByteForge"],
    "Home": ["Maison Lumiere", "Decor & Co", "Habitat Plus"],
    "Beauty": ["Beaute Naturelle", "Eclat Paris", "Soin Doux"],
    "Food": ["Terroir Select", "Gourmet France", "Bio Delice"]
}

products = []
for i in range(1, 501):
    cat = random.choice(list(categories.keys()))
    name = random.choice(categories[cat])
    brand = random.choice(brands[cat])
    sku = f"{cat[:3].upper()}-{i:04d}"
    base_price = round(random.uniform(5, 200), 2)
    cost = round(base_price * random.uniform(0.3, 0.7), 2)
    weight_kg = round(random.uniform(0.1, 15.0), 2)
    in_stock = random.random() > 0.05
    products.append(Row(
        product_id=i, product_name=f"{brand} {name}", sku=sku,
        category=cat, brand=brand, unit_price=base_price, unit_cost=cost,
        weight_kg=weight_kg, is_in_stock=in_stock,
        created_date=random_date(datetime(2022, 1, 1), datetime(2024, 6, 1)).date()
    ))

df_products = spark.createDataFrame(products)
df_products.write.mode("overwrite").saveAsTable("products")
print(f"products: {df_products.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stores

# COMMAND ----------

store_cities = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier",
                "Bordeaux", "Lille", "Rennes", "Reims", "Toulon", "Grenoble", "Dijon", "Angers",
                "Nimes", "Clermont-Ferrand", "Le Havre", "Aix-en-Provence"] * 3  # repeat for 50+
store_types = ["Flagship", "Standard", "Outlet", "Pop-up"]

stores = []
for i in range(1, 51):
    city = store_cities[i - 1] if i <= len(store_cities) else random.choice(cities)
    stype = random.choices(store_types, weights=[0.15, 0.50, 0.25, 0.10], k=1)[0]
    sqm = random.randint(80, 2000) if stype != "Pop-up" else random.randint(20, 80)
    opened = random_date(datetime(2015, 1, 1), datetime(2024, 12, 31))
    stores.append(Row(
        store_id=i, store_name=f"Store {city} {i}", city=city,
        region=regions.get(city, "Other"), store_type=stype,
        surface_sqm=sqm, opening_date=opened.date(),
        manager_name=f"{random.choice(first_names_m + first_names_f)} {random.choice(last_names)}"
    ))

df_stores = spark.createDataFrame(stores)
df_stores.write.mode("overwrite").saveAsTable("stores")
print(f"stores: {df_stores.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Suppliers

# COMMAND ----------

supplier_countries = ["France", "Germany", "Italy", "Spain", "Portugal", "China", "Vietnam", "Turkey", "India", "Morocco"]
supplier_specialties = ["Apparel", "Electronics", "Home", "Beauty", "Food", "Packaging", "Logistics"]

suppliers = []
for i in range(1, 101):
    country = random.choice(supplier_countries)
    specialty = random.choice(supplier_specialties)
    lead_days = random.randint(2, 45)
    rating = round(random.uniform(2.5, 5.0), 1)
    certified = random.random() > 0.3
    suppliers.append(Row(
        supplier_id=i,
        supplier_name=f"Supplier_{i:03d}_{country[:3].upper()}",
        country=country, specialty=specialty,
        lead_time_days=lead_days, quality_rating=rating,
        is_certified=certified,
        contract_start=random_date(datetime(2020, 1, 1), datetime(2024, 1, 1)).date(),
        annual_volume_eur=random.randint(50000, 5000000)
    ))

df_suppliers = spark.createDataFrame(suppliers)
df_suppliers.write.mode("overwrite").saveAsTable("suppliers")
print(f"suppliers: {df_suppliers.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Orders

# COMMAND ----------

channels = ["Web", "Store", "Mobile App"]
statuses = ["Completed", "Shipped", "Processing", "Cancelled", "Returned"]
status_weights = [0.55, 0.15, 0.10, 0.12, 0.08]

orders = []
for i in range(1, 25001):
    cust_id = random.randint(1, 5000)
    store_id = random.randint(1, 50) if random.random() > 0.4 else None
    channel = "Store" if store_id and random.random() > 0.3 else random.choice(["Web", "Mobile App"])
    status = random.choices(statuses, weights=status_weights, k=1)[0]
    order_ts = random_ts(DATE_START, DATE_END)
    orders.append(Row(
        order_id=i, customer_id=cust_id, store_id=store_id,
        order_channel=channel, order_status=status,
        order_timestamp=order_ts,
        shipping_address_city=random.choice(cities),
        discount_pct=random.choice([0, 0, 0, 5, 10, 15, 20, 25])
    ))

df_orders = spark.createDataFrame(orders)
df_orders.write.mode("overwrite").saveAsTable("orders")
print(f"orders: {df_orders.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Order Items

# COMMAND ----------

order_items = []
item_id = 0
for oid in range(1, 25001):
    n_items = random.choices([1, 2, 3, 4, 5], weights=[0.35, 0.30, 0.20, 0.10, 0.05], k=1)[0]
    used_products = set()
    for _ in range(n_items):
        pid = random.randint(1, 500)
        while pid in used_products:
            pid = random.randint(1, 500)
        used_products.add(pid)
        item_id += 1
        qty = random.choices([1, 2, 3, 4, 5], weights=[0.50, 0.25, 0.15, 0.07, 0.03], k=1)[0]
        # price will be looked up via join in the lab; store a snapshot here
        unit_price = round(random.uniform(5, 200), 2)
        order_items.append(Row(
            item_id=item_id, order_id=oid, product_id=pid,
            quantity=qty, unit_price_snapshot=unit_price,
            line_total=round(unit_price * qty, 2)
        ))

# Create in batches to avoid driver OOM
batch_size = 25000
df_items = None
for start in range(0, len(order_items), batch_size):
    batch = spark.createDataFrame(order_items[start:start + batch_size])
    df_items = batch if df_items is None else df_items.union(batch)

df_items.write.mode("overwrite").saveAsTable("order_items")
print(f"order_items: {df_items.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Bonus: CSV file for drag-and-drop exercise
# MAGIC
# MAGIC Creates a small CSV in a Unity Catalog Volume for the file-upload lab exercise.

# COMMAND ----------

spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.lab_files")

promotions = []
for i in range(1, 21):
    start = random_date(datetime(2025, 1, 1), datetime(2026, 3, 1))
    end = start + timedelta(days=random.randint(3, 30))
    promotions.append(Row(
        promo_id=i,
        promo_name=f"Promo {random.choice(['Spring', 'Summer', 'Winter', 'Flash', 'Weekend', 'Holiday', 'Clearance', 'VIP'])} {i}",
        discount_pct=random.choice([10, 15, 20, 25, 30, 40, 50]),
        start_date=str(start.date()),
        end_date=str(end.date()),
        applicable_category=random.choice(["Apparel", "Electronics", "Home", "Beauty", "Food", "All"])
    ))

df_promos = spark.createDataFrame(promotions)
df_promos.toPandas().to_csv(f"/Volumes/{CATALOG}/{SCHEMA}/lab_files/promotions.csv", index=False)
print("promotions.csv written to Volume")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify

# COMMAND ----------

for table in ["customers", "products", "stores", "suppliers", "orders", "order_items"]:
    count = spark.table(table).count()
    print(f"  {CATALOG}.{SCHEMA}.{table}: {count:,} rows")

print("\nAll tables ready. Open Lakeflow Designer and start the lab!")
