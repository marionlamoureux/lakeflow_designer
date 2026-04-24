# Lakeflow Designer - Hands-On Lab

**A no-code, visual data preparation tool built into Databricks -- governed, scalable, AI-assisted.**

This lab demonstrates Lakeflow Designer through a realistic finance/CFT scenario: OTC derivatives reconciliation, break detection, and regulatory reporting. It is designed for teams evaluating Lakeflow Designer as an alternative to tools like Alteryx in a context where governance and traceability (e.g., ECB requirements) are critical.

## Prerequisites

| Requirement | Details |
|---|---|
| Databricks workspace | Unity Catalog enabled, serverless compute available |
| Permissions | `CAN USE` on at least one compute resource |
| AI features | Databricks AI Assistive features enabled |
| Catalog | A catalog + schema you can write to (lab uses `lab_lakeflow.cft`) |

## Lab Structure

| # | Module | Duration | Key Features |
|---|---|---|---|
| 0 | Setup & Data Generation | 10 min | Run notebook to create test tables + Excel file |
| 1 | First Visual Data Prep | 10 min | UC table source + **Excel drag-and-drop** (the key pattern) |
| 2 | Filtering & Sorting | 10 min | Filter, Sort, Limit operators |
| 3 | Transforms & Genie Code AI | 15 min | Custom columns, natural language expressions |
| 4 | Joins | 10 min | Multi-table joins, break detection (trades vs settlements) |
| 5 | Aggregations | 10 min | Aggregate functions, exposure reports |
| 6 | Combine & Reshape | 10 min | Union, Intersect, Except, Pivot/Unpivot |
| 7 | SQL & Python Operators | 10 min | Window functions, PySpark risk calculations |
| 8 | Output, Lineage & Schedule | 10 min | Write to UC, view lineage graph, scheduling |
| 9 | End-to-End Pipeline | 15 min | Full regulatory report: trades + Excel adjustments + breaks |

**Total: ~2 hours**

## Quick Start

1. **Generate test data**: Import `data_generation/00_generate_test_data.py` into a Databricks notebook and run it.
2. **Download the Excel file**: Get `regulatory_adjustments.xlsx` from the Volume to your desktop.
3. **Follow the lab**: Open `lab_guide/lab_guide.md` and follow step by step.

## Dataset

Finance/CFT scenario with 4 UC tables + 1 Excel file:

- `counterparties` (200 rows) - Banks, corporates, funds with LEI, ratings, netting agreements
- `otc_trades` (10,000 rows) - OTC derivatives (IRS, CDS, FX Fwd, Options) with MTM, notionals
- `settlements` (9,500 rows) - Settlement records (~500 trades have no settlement = breaks)
- `market_data` (80 rows) - Daily risk factors (rates, spreads, FX) for 4 reporting dates
- `regulatory_adjustments.xlsx` - **Excel file** with manual MTM adjustments from business team (drag-and-drop onto canvas)

## Demo Flow (for presenters)

The suggested demo follows this narrative:

1. **Ingest**: UC table + drag-and-drop Excel file (demonstrates industrializing ad-hoc business inputs)
2. **No-code transforms**: Join, filter, aggregate, custom columns -- all visual, no code
3. **Genie Code**: Natural language to generate expressions (the differentiator)
4. **Output**: Write to governed UC table
5. **Lineage**: Show the lineage graph in Unity Catalog (key for regulatory traceability)
6. **Genie Q&A**: Data exploration with natural language

## Repository Structure

```
lakeflow_designer/
  README.md                          # This file
  data_generation/
    00_generate_test_data.py         # Databricks notebook - creates all test data + Excel
  lab_guide/
    lab_guide.md                     # Step-by-step hands-on instructions
  deck/
    lakeflow_designer_deck.md        # Marp presentation deck
  resources/
    alteryx_comparison.md            # Detailed Alteryx vs Lakeflow Designer comparison
```
