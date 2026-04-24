# Lakeflow Designer - Hands-On Lab Guide

> **Audience:** Data analysts and engineers evaluating Lakeflow Designer as an Alteryx replacement.
> **Dataset:** Retail supply chain (customers, products, stores, suppliers, orders, order_items).
> **Workspace prerequisite:** Run `data_generation/00_generate_test_data.py` first.

---

## Module 0 - Setup & Data Verification

### 0.1 Run the data generation notebook

1. In your Databricks workspace, click **New > Notebook**.
2. Copy-paste or import `data_generation/00_generate_test_data.py`.
3. Attach to a cluster (serverless recommended) and **Run All**.
4. Confirm you see 6 tables in `lab_lakeflow.retail`.

### 0.2 Verify Unity Catalog access

```sql
USE CATALOG lab_lakeflow;
USE SCHEMA retail;
SHOW TABLES;
```

You should see: `customers`, `products`, `stores`, `suppliers`, `orders`, `order_items`.

### 0.3 Check the CSV volume

```sql
LIST '/Volumes/lab_lakeflow/retail/lab_files/';
```

You should see `promotions.csv`.

---

## Module 1 - Your First Visual Data Prep

> **Goal:** Learn canvas basics, add a Source, navigate, and preview data.

### 1.1 Create a new Visual Data Prep

1. In the sidebar, click **New > Visual data prep**.
2. The welcome screen appears with the option to select a source.

### 1.2 Add a Source operator

1. Click **Select source** and browse to `lab_lakeflow.retail.customers`.
2. The Source operator appears on the canvas.
3. Click on the operator -- the **output pane** at the bottom shows a data preview (up to 1,000 rows).

### 1.3 Explore the canvas

| Action | How |
|---|---|
| Pan | Hold `Space` + drag |
| Zoom | `Ctrl/Cmd` + scroll wheel |
| Fit view | Click the fit-to-view button (top toolbar) |
| Auto-layout | Click the auto-layout button (top toolbar) |
| Undo / Redo | `Cmd/Ctrl + Z` / `Cmd/Ctrl + Shift + Z` |

### 1.4 Data profiling

1. With the customers Source selected, look at the output pane.
2. Click the **sidebar icon** (top-right of the output pane) to open **Data Profiling**.
3. Explore the distribution graphs for `age`, `loyalty_tier`, `city`.
4. Click on a column header to see stats: count, distinct values, nulls, min/max.

### 1.5 Sample vs Full dataset

1. Notice the toggle at the top of the output pane: **Sample dataset** (default).
2. Switch to **Full dataset** and click **Run**. The preview now shows all 5,000 rows.
3. Switch back to **Sample dataset** for faster iteration.

> **Alteryx comparison:** This replaces the Browse tool. Unlike Alteryx which must run the entire workflow to see results, Lakeflow Designer shows instant previews on sample data at every step.

---

## Module 2 - Filtering & Sorting

> **Goal:** Master the Filter, Sort, and Limit operators.

### 2.1 Filter operator - Basic

1. Click the **+** button on the right side of the customers Source operator.
2. Select **Filter** from the operator menu.
3. Configure the filter:
   - Column: `is_active`
   - Condition: `Is equal to`
   - Value: `true`
4. Check the output pane -- only active customers remain.

### 2.2 Filter operator - Multiple conditions

1. In the same Filter operator, click **+ Add condition**.
2. Add: Column: `loyalty_tier`, Condition: `Is one of`, Values: `Gold, Platinum`.
3. The output now shows only active Gold/Platinum customers.

> **Tip:** Conditions are combined with AND logic by default.

### 2.3 Filter operator - Text matching

1. Add a **new** Filter after the first one (click **+** on the Filter output).
2. Configure: Column: `city`, Condition: `Contains`, Value: `Paris`.
3. Preview the results -- only Parisian Gold/Platinum active customers.

### 2.4 Sort operator

1. Click **+** on the last Filter and select **Sort**.
2. Sort by `age` in **DESC** (descending) order.
3. Click **+ Add sort expression** and add `last_name` **ASC** as a secondary sort.
4. Preview the sorted output.

### 2.5 Limit operator

1. Add a **Limit** operator after the Sort.
2. Set the row limit to `100`.
3. Preview: you now see the top 100 oldest Gold/Platinum active customers in Paris.

> **Alteryx comparison:** Filter = Alteryx Filter. Sort = Alteryx Sort. Limit = Alteryx Sample. The difference: no need to run the workflow first; results are instant.

---

## Module 3 - Transforms & Expressions

> **Goal:** Use the Transform operator, create custom columns, and leverage Genie Code AI.

### 3.1 Start a new Visual Data Prep

1. Create a new Visual data prep (**New > Visual data prep**).
2. Add Source: `lab_lakeflow.retail.products`.

### 3.2 Transform - Select and rename columns

1. Add a **Transform** operator.
2. In the configuration pane:
   - **Uncheck** `created_date` (exclude it from output).
   - **Rename** `unit_price` to `retail_price`.
   - **Rename** `unit_cost` to `cost_price`.
   - **Reorder**: drag `category` above `brand`.
3. Preview the result.

### 3.3 Transform - Custom column (manual expression)

1. In the same Transform operator, click **+ Add a custom column**.
2. Name: `profit_margin_pct`
3. In the **Expression** field, type:
   ```
   round((retail_price - cost_price) / retail_price * 100, 1)
   ```
4. Preview the new column. Each product now has a margin percentage.

### 3.4 Transform - Custom column with Genie Code AI

1. Click **+ Add a custom column** again.
2. Name: `price_category`
3. In the **Description** field (natural language), type:
   ```
   Categorize the retail price: "Budget" if under 30, "Mid-range" if 30-100, "Premium" if over 100
   ```
4. Watch Genie generate the expression automatically.
5. Review the generated code and preview the result.

### 3.5 Genie Code - Open conversation

1. Open the **Genie Code** panel (AI assistant icon on the canvas).
2. Type: `Add a column called margin_category that labels products as "Low Margin" if profit_margin_pct < 30, "Medium Margin" if between 30-60, and "High Margin" if above 60`
3. Genie adds the transformation. Review the operator it created.
4. Try another prompt: `Flag products where weight_kg is above 10 as "Heavy" and the rest as "Light"`

### 3.6 Genie Code - Image upload

1. Take a screenshot of a spreadsheet formula or an Alteryx workflow you want to replicate.
2. Upload it via the **image upload button** in Genie Code.
3. Ask Genie: `Replicate this logic in my pipeline`.

> **Alteryx comparison:** Transform = Alteryx Select + Formula tools combined. Genie Code is a major differentiator -- Alteryx has no AI-assisted expression builder.

---

## Module 4 - Joins

> **Goal:** Join multiple tables like you would in Alteryx.

### 4.1 Set up the join

1. Create a new Visual data prep.
2. Add **two** Source operators:
   - Source 1: `lab_lakeflow.retail.orders`
   - Source 2: `lab_lakeflow.retail.customers`

### 4.2 Inner Join

1. Add a **Join** operator from the menu.
2. Connect the output of `orders` to the left input of the Join.
3. Connect the output of `customers` to the right input of the Join.
4. Configure:
   - Join condition: `orders.customer_id = customers.customer_id`
   - Join type: **Inner join**
5. Preview the result. Notice that columns from both tables appear.

### 4.3 Column selection in Join

1. In the Join configuration, scroll to the **Output columns** section.
2. Uncheck duplicate columns (e.g., the second `customer_id`).
3. Keep only the columns you need: `order_id`, `order_timestamp`, `order_status`, `first_name`, `last_name`, `loyalty_tier`.

### 4.4 Left Join

1. Change the join type to **Left join**.
2. Preview: all orders appear, including those where `customer_id` might not match (nulls on the customer side).

### 4.5 Multi-table join

1. Add a third Source: `lab_lakeflow.retail.stores`.
2. Add another **Join** operator after the first Join.
3. Connect the first Join's output to the left input.
4. Connect `stores` to the right input.
5. Join on: `orders.store_id = stores.store_id`.
6. Use a **Left join** (some orders may not have a store -- web/mobile orders).
7. Preview the enriched dataset.

### 4.6 Add a custom expression in Join

1. In the second Join, click **+ Add custom expression column**.
2. Name: `order_channel_detail`
3. Expression:
   ```
   CASE WHEN store_name IS NOT NULL THEN concat('In-store: ', store_name) ELSE order_channel END
   ```
4. Preview.

> **Alteryx comparison:** Join operator = Alteryx Join tool. Multiple joins chain naturally. The custom expression column in the Join is a bonus Alteryx doesn't have natively.

---

## Module 5 - Aggregations

> **Goal:** Summarize data with grouping and aggregate functions.

### 5.1 Revenue by customer

1. Continue from Module 4 or start a new Visual data prep with `order_items` and `orders` as sources.
2. Join `order_items` to `orders` on `order_id`.
3. Add an **Aggregate** operator after the Join.
4. Configure:
   - **Group by:** `customer_id`
   - **Aggregations:**
     - `line_total` > **SUM** > name it `total_revenue`
     - `item_id` > **COUNT** > name it `total_items`
     - `line_total` > **AVG** > name it `avg_order_value`
5. Preview the customer summary.

### 5.2 Multiple groupings

1. Add a second Aggregate operator.
2. Group by: `order_status`
3. Aggregations:
   - `order_id` > **COUNT** > `order_count`
   - `line_total` > **SUM** > `total_value`
   - `line_total` > **MEDIAN** > `median_value`
4. Preview.

### 5.3 Advanced aggregations

1. Create a new Aggregate:
   - Group by: `product_id`
   - Aggregations:
     - `quantity` > **SUM** > `total_units_sold`
     - `line_total` > **SUM** > `total_revenue`
     - `unit_price_snapshot` > **STDDEV** > `price_volatility`
     - `unit_price_snapshot` > **VARIANCE** > `price_variance`
     - `quantity` > **PERCENTILE** (configure: 90th) > `qty_p90`
2. Preview.

> **Available aggregation functions:** AVG, COUNT, MAX, MEAN, MEDIAN, MIN, PERCENTILE, STDDEV, SUM, VARIANCE
>
> **Alteryx comparison:** Aggregate = Alteryx Summarize tool. All standard functions plus PERCENTILE, STDDEV, and VARIANCE which require the R or Python tool in Alteryx.

---

## Module 6 - Combine & Reshape

> **Goal:** Use Union, Intersect, Except, and Pivot/Unpivot.

### 6.1 Combine - Union

1. Create a new Visual data prep.
2. Add two Source operators:
   - Source 1: filter `orders` where `order_channel = 'Web'`
   - Source 2: filter `orders` where `order_channel = 'Mobile App'`
   (Use a Filter operator after each Source to apply the condition.)
3. Add a **Combine** operator and connect both filtered outputs.
4. Set operation: **Union** / **All** (keep duplicates).
5. Preview -- you now have all digital orders combined.

### 6.2 Combine - Intersect

1. Create two filtered customer sets:
   - Set A: customers in `Ile-de-France`
   - Set B: customers with `loyalty_tier = 'Gold'`
2. Use a Transform on each to select only `customer_id`, `first_name`, `last_name`.
3. Combine with **Intersect** > **Distinct**.
4. Preview: only Gold customers who live in Ile-de-France.

### 6.3 Combine - Except

1. Same setup as 6.2.
2. Change operation to **Except** > **Distinct**.
3. Preview: Ile-de-France customers who are NOT Gold tier.

### 6.4 Pivot (Rows to Columns)

1. Start from an Aggregate that shows `order_count` grouped by `order_channel` and `order_status`.
2. Add a **Pivot** operator (may appear as **Reshape**).
3. Mode: **Rows to Columns**.
4. Pivot column: `order_status`
5. Value column: `order_count`
6. Aggregation: **SUM**
7. Preview: each row is a channel, columns are statuses with counts.

### 6.5 Unpivot (Columns to Rows)

1. On the pivoted output, add another Pivot operator.
2. Mode: **Columns to Rows**.
3. Select the status columns to unpivot.
4. Configure key column name: `status` and value column name: `count`.
5. Preview: the data is back in long format.

> **Alteryx comparison:** Combine = Alteryx Union. Pivot = Alteryx Cross Tab. Unpivot = Alteryx Transpose. In Alteryx these are 3 separate tools; in Lakeflow Designer, Combine handles Union/Intersect/Except and Pivot handles both directions.

---

## Module 7 - SQL & Python Operators

> **Goal:** Use custom SQL and PySpark when built-in operators aren't enough.

### 7.1 SQL operator

1. In any Visual data prep, add a **SQL** operator after a Source or Transform.
2. The SQL operator lets you write a custom `SELECT` statement.
3. Upstream operators are referenced by their **operator name** as table identifiers.
4. Example: if your Source is named `customers`, write:
   ```sql
   SELECT
     customer_id,
     first_name || ' ' || last_name AS full_name,
     DATEDIFF(CURRENT_DATE(), signup_date) AS days_since_signup,
     CASE
       WHEN age < 25 THEN 'Gen Z'
       WHEN age < 40 THEN 'Millennial'
       WHEN age < 55 THEN 'Gen X'
       ELSE 'Boomer'
     END AS generation
   FROM customers
   WHERE is_active = true
   ```
5. Preview the result.

### 7.2 SQL - Window functions

1. Add another SQL operator and write:
   ```sql
   SELECT *,
     RANK() OVER (PARTITION BY generation ORDER BY days_since_signup DESC) AS tenure_rank,
     COUNT(*) OVER (PARTITION BY generation) AS generation_count
   FROM sql_operator_1
   ```
   (Replace `sql_operator_1` with the actual name of the upstream operator.)
2. This demonstrates window functions that would require Alteryx's Multi-Row Formula or Summarize + Join.

### 7.3 Python operator

1. Add a **Python** operator.
2. Your input data is available as `inputs["data"]` (a list of DataFrames, typically `inputs["data"][0]`).
3. Write PySpark code:
   ```python
   from pyspark.sql import functions as F

   df = inputs["data"][0]

   # Add a column with a complex calculation
   result = df.withColumn(
       "loyalty_score",
       F.when(F.col("generation") == "Gen Z", F.col("days_since_signup") * 1.5)
        .when(F.col("generation") == "Millennial", F.col("days_since_signup") * 1.2)
        .otherwise(F.col("days_since_signup") * 1.0)
   ).withColumn(
       "loyalty_score_normalized",
       F.round(F.col("loyalty_score") / F.lit(365), 2)
   )
   ```
4. The variable `result` is the output DataFrame.
5. Preview.

> **Alteryx comparison:** SQL operator = a massive upgrade over Alteryx's in-database tools. Python operator = Alteryx Python tool but running on Spark (distributed, not single-machine pandas).

---

## Module 8 - Output, Publish & Schedule

> **Goal:** Write results to Unity Catalog tables and automate the pipeline.

### 8.1 Add an Output operator

1. In any pipeline, click **+** on the last operator.
2. Select **Output** (target).
3. Configure:
   - Catalog: `lab_lakeflow`
   - Schema: `retail`
   - Table name: `gold_customer_summary`
4. Click **Run** to materialize the table.

### 8.2 Verify the output

```sql
SELECT * FROM lab_lakeflow.retail.gold_customer_summary LIMIT 10;
```

### 8.3 Schedule the pipeline

1. Click the **Schedule** button in the top toolbar.
2. Configure:
   - Frequency: Daily, Weekly, or Cron expression
   - Cluster: serverless (recommended)
3. Save the schedule.

### 8.4 Integrate into a Databricks Job

1. Go to **Workflows > Jobs > Create Job**.
2. Add a task of type **Visual data prep**.
3. Select your saved Visual data prep.
4. Add additional tasks (notebooks, SQL, other pipelines) to build a complete orchestrated workflow.
5. This is how you build production-grade data pipelines that replace Alteryx Server.

> **Alteryx comparison:** Output = Alteryx Output Data tool, but writes directly to governed Unity Catalog tables. Schedule = Alteryx Scheduler / Server, but integrated with Databricks Jobs for multi-step orchestration that Alteryx Server cannot match.

---

## Module 9 - End-to-End Pipeline: Alteryx Replacement Workflow

> **Goal:** Build a complete pipeline that mimics a typical Alteryx workflow -- from raw data to business-ready output.

### Scenario

Your business team needs a **Weekly Sales Performance Report** with:
- Revenue by store and product category
- Customer loyalty tier breakdown
- Top 10 products by revenue
- Comparison of online vs in-store sales

### Step-by-step

#### 1. Sources (3 inputs)
Add three Source operators:
- `lab_lakeflow.retail.order_items`
- `lab_lakeflow.retail.orders`
- `lab_lakeflow.retail.products`

#### 2. Join order_items to orders
- Join on `order_id`
- Keep: `order_id`, `product_id`, `quantity`, `line_total`, `order_timestamp`, `order_status`, `order_channel`, `store_id`, `customer_id`, `discount_pct`

#### 3. Join to products
- Join on `product_id`
- Keep: add `product_name`, `category`, `brand`, `unit_cost`

#### 4. Filter completed orders
- Filter: `order_status` = `Completed`

#### 5. Transform - Add calculated columns
Use Genie Code:
- Prompt: `Add columns: gross_profit = line_total - (unit_cost * quantity), order_month = date_format(order_timestamp, 'yyyy-MM')`

#### 6. Branch 1: Revenue by category and channel
- Aggregate: Group by `category`, `order_channel`. Sum `line_total` as `revenue`, Sum `gross_profit` as `profit`, Count `order_id` as `order_count`.
- Pivot: Rows to Columns on `order_channel`, value = `revenue`, aggregation = SUM.
- Output: write to `lab_lakeflow.retail.report_revenue_by_category`

#### 7. Branch 2: Top products
- Aggregate: Group by `product_id`, `product_name`, `category`. Sum `line_total` as `total_revenue`, Sum `quantity` as `total_units`.
- Sort: `total_revenue` DESC.
- Limit: 10 rows.
- Output: write to `lab_lakeflow.retail.report_top_products`

#### 8. Branch 3: Monthly trend
- Aggregate: Group by `order_month`. Sum `line_total` as `monthly_revenue`, Count distinct `customer_id` as `unique_customers`.
- Sort: `order_month` ASC.
- Output: write to `lab_lakeflow.retail.report_monthly_trend`

#### 9. Run and verify

```sql
SELECT * FROM lab_lakeflow.retail.report_revenue_by_category;
SELECT * FROM lab_lakeflow.retail.report_top_products;
SELECT * FROM lab_lakeflow.retail.report_monthly_trend;
```

#### 10. Schedule
Schedule this pipeline to run weekly.

---

## Bonus Exercises

### Drag-and-drop CSV
1. Download `promotions.csv` from the Volume (or use the one in `data_generation/`).
2. Drag it onto the canvas of any Visual data prep.
3. A Source operator is automatically created.
4. Join it to your orders data on date ranges.

### Genie Code advanced prompts
Try these prompts in the Genie Code assistant:
- `Show me the distribution of order values by loyalty tier`
- `Create a cohort analysis based on customer signup month`
- `Find customers who haven't ordered in the last 6 months`
- `Calculate month-over-month revenue growth`
- `@lab_lakeflow.retail.customers - which regions have the highest concentration of Platinum customers?`

### Google Drive / SharePoint import
1. Upload a CSV to Google Drive.
2. In a Source operator, select **Google Drive** and paste the file URL.
3. You need a Unity Catalog connection for Google Drive configured by your admin.

---

## Appendix: Genie Code Prompt Library

Effective prompts for common Alteryx-replacement tasks:

| Task | Prompt |
|---|---|
| Dedup | `Remove duplicate rows based on customer_id, keeping the most recent order` |
| Type cast | `Convert the order_date column from string to date format yyyy-MM-dd` |
| Null handling | `Replace null values in discount_pct with 0 and in shipping_address_city with 'Unknown'` |
| String cleanup | `Trim whitespace, capitalize first letter of first_name and last_name` |
| Regex extract | `Extract the numeric part from the SKU column into a new column called sku_number` |
| Date math | `Add a column days_to_deliver calculated as datediff between delivery_date and order_date` |
| Running total | `Add a running total of line_total partitioned by customer_id ordered by order_timestamp` |
| Fuzzy match | `Find customer names that are similar using soundex on last_name` |
| Rank | `Rank products by total_revenue within each category` |
| Binning | `Create age bins: 18-25, 26-35, 36-50, 51-65, 65+` |
