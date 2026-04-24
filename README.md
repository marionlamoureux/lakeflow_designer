# Lakeflow Designer - Hands-On Lab

**Replace Alteryx with a governed, scalable, visual ETL on Databricks.**

This lab walks through every major Lakeflow Designer feature using a realistic retail supply chain dataset. By the end, participants will have built a complete data pipeline visually -- no code required -- while understanding how each capability maps to (and exceeds) what they do in Alteryx today.

## Prerequisites

| Requirement | Details |
|---|---|
| Databricks workspace | Unity Catalog enabled, serverless compute available |
| Permissions | `CAN USE` on at least one compute resource |
| AI features | Databricks AI Assistive features enabled |
| Catalog | A catalog + schema you can write to (lab uses `lab_lakeflow`) |

## Lab Structure

| # | Module | Duration | Key Features |
|---|---|---|---|
| 0 | Setup & Data Generation | 10 min | Run notebook to create test tables |
| 1 | First Visual Data Prep | 10 min | Canvas basics, Source operator, navigation, preview |
| 2 | Filtering & Sorting | 10 min | Filter operator, Sort, Limit |
| 3 | Transforms & Expressions | 15 min | Transform operator, custom columns, Genie Code AI |
| 4 | Joins | 10 min | Join operator, join types, column selection |
| 5 | Aggregations | 10 min | Aggregate operator, grouping, aggregate functions |
| 6 | Combine & Reshape | 10 min | Combine (Union/Intersect/Except), Pivot/Unpivot |
| 7 | SQL & Python Operators | 10 min | Custom SQL, PySpark code |
| 8 | Output, Publish & Schedule | 10 min | Target tables, scheduling, Jobs integration |
| 9 | End-to-End Pipeline | 15 min | Build a complete Alteryx-replacement workflow |

**Total estimated time: ~2 hours**

## Quick Start

1. **Generate test data**: Import `data_generation/00_generate_test_data.py` into a Databricks notebook and run it.
2. **Open the lab guide**: Follow `lab_guide/lab_guide.md` step by step.
3. **Presentation deck**: Use `deck/lakeflow_designer_deck.md` (Marp-compatible markdown) or import the content into Google Slides.

## Dataset Overview

The lab uses a **retail supply chain** dataset with 6 interrelated tables:

- `customers` - 5,000 customers with demographics and loyalty tiers
- `products` - 500 products across categories (apparel, electronics, home, beauty, food)
- `stores` - 50 store locations across France
- `orders` - 25,000 orders over the past 2 years
- `order_items` - 75,000 line items with quantities and prices
- `suppliers` - 100 suppliers with lead times and ratings

This mirrors a typical Alteryx user's world: CRM exports, ERP extracts, and spreadsheet data that needs joining, cleaning, aggregating, and publishing.

## Alteryx Feature Mapping

| Alteryx Tool | Lakeflow Designer Equivalent |
|---|---|
| Input Data | Source operator (UC tables, volumes, CSV/Excel drag-drop, Google Drive, SharePoint) |
| Filter | Filter operator |
| Sort | Sort operator |
| Sample | Limit operator + Sample dataset toggle |
| Select / Rename | Transform operator |
| Formula | Transform > Custom column (with Genie AI code generation) |
| Join | Join operator (Inner, Left, Right, Full) |
| Union | Combine operator (Union/Intersect/Except) |
| Summarize | Aggregate operator (SUM, AVG, COUNT, MIN, MAX, MEDIAN, STDDEV, VARIANCE, PERCENTILE) |
| Cross Tab / Transpose | Pivot operator (Rows-to-Columns / Columns-to-Rows) |
| Output Data | Output operator (write to Unity Catalog tables) |
| Scheduler | Built-in Schedule button + Databricks Jobs |
| Alteryx Gallery | Databricks workspace sharing + Git integration |
| Python tool | Python operator (PySpark) |
| Custom SQL | SQL operator |
| Browse | Output pane preview + Data profiling sidebar |

## Repository Structure

```
lakeflow_designer/
  README.md                          # This file
  data_generation/
    00_generate_test_data.py         # Databricks notebook - creates all test tables
  lab_guide/
    lab_guide.md                     # Step-by-step hands-on instructions
  deck/
    lakeflow_designer_deck.md        # Marp presentation deck (markdown)
  resources/
    alteryx_comparison.md            # Detailed Alteryx vs Lakeflow Designer comparison
```
