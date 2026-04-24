---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  }
  h1 {
    color: #FF3621;
  }
  h2 {
    color: #1B3139;
  }
  table {
    font-size: 0.75em;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1em;
  }
---

<!-- _class: lead -->

# Lakeflow Designer
## Visual ETL on Databricks
### From Alteryx to Governed, Scalable Data Pipelines

---

# Agenda

1. Why rethink your ETL tooling?
2. What is Lakeflow Designer?
3. Core capabilities deep dive
4. Alteryx vs Lakeflow Designer
5. Live demo / Hands-on lab
6. Architecture & governance
7. Next steps

---

# The Challenge with Alteryx

- **Desktop-bound**: workflows run on a single machine, limited scalability
- **Governance gap**: no native Unity Catalog, no lineage, manual version control
- **Costly licensing**: per-seat model with separate Server costs
- **Data movement**: data exported/imported between tools, creating silos
- **AI gap**: no built-in AI-assisted development

> "We spend more time managing Alteryx infrastructure than building pipelines."

---

# What is Lakeflow Designer?

A **visual, drag-and-drop ETL canvas** built into the Databricks platform.

- Build data pipelines visually -- no code required
- Every transformation is **backed by code** (reproducible, auditable)
- Runs on **serverless compute** (no infrastructure to manage)
- Native **Unity Catalog** integration (governance from day one)
- **Genie Code AI** assistant for natural language transformations
- Publish, schedule, and orchestrate as part of Databricks Jobs

**Status:** Public Preview (April 2026)

---

# How It Works

```
  Source         Transform        Aggregate       Output
  [UC Table] --> [Filter/Join] --> [Group/Sum] --> [UC Table]
  [CSV file]     [Custom col]     [Pivot]         [Schedule]
  [Drive]        [SQL/Python]     [Sort/Limit]    [Job task]
```

- **Canvas**: drag-and-drop operators arranged as a DAG
- **Data flows left to right** through connected operators
- **Instant previews** on 1,000-row samples at every step
- **Full dataset execution** when you're ready for production

---

# Core Operators

| Operator | Purpose | Alteryx Equivalent |
|---|---|---|
| **Source** | Read from UC tables, volumes, CSV/Excel, Google Drive, SharePoint | Input Data |
| **Filter** | Row-level filtering with graphical conditions | Filter |
| **Transform** | Select, rename, reorder, add custom columns | Select + Formula |
| **Join** | Combine tables (Inner, Left, Right, Full) | Join |
| **Combine** | Union, Intersect, Except | Union |
| **Aggregate** | Group by + SUM, AVG, COUNT, MEDIAN, STDDEV... | Summarize |
| **Pivot** | Rows-to-Columns and Columns-to-Rows | Cross Tab + Transpose |
| **Sort / Limit** | Order and cap row count | Sort + Sample |
| **SQL** | Custom SELECT statements | In-DB tools |
| **Python** | PySpark code | Python tool (but distributed) |
| **Output** | Write to Unity Catalog table | Output Data |

---

# Feature: Source Operator

**Multiple data source types:**
- Browse Unity Catalog tables and volumes
- Drag-and-drop CSV or Excel files onto the canvas
- Google Drive (via UC connection)
- SharePoint (via UC connection)
- Lakeflow Connect for SaaS sources (Salesforce, Workday, HubSpot...)

**vs Alteryx:** No drivers to install, no ODBC config, no file path management. Everything is governed through Unity Catalog.

---

# Feature: Filter Operator

**Graphical condition builder -- no expressions needed**

Condition types:
- Equality: Is equal to / Is not equal to
- Sets: Is one of / Is not one of
- Text: Contains, Starts with, Ends with
- Numeric: Greater than, Less than
- Null: Is null / Is not null
- Multiple conditions with AND logic

**vs Alteryx:** Same functionality as the Filter tool, but with instant preview of results before running.

---

# Feature: Transform Operator

**The Swiss Army knife -- replaces 2+ Alteryx tools:**

- **Select** columns (include/exclude checkboxes)
- **Rename** columns inline
- **Reorder** columns by drag-and-drop
- **Custom columns** with expression editor
  - Write code directly **OR**
  - Describe in natural language -- Genie generates the code

**vs Alteryx:** Combines Select + Formula + Multi-Field Formula. The AI-generated expressions are a major differentiator.

---

# Feature: Genie Code AI Assistant

**Natural language to transformation -- the killer feature**

- Describe what you want in plain English (or French)
- Genie generates the Spark SQL / PySpark expression
- Context-aware: knows your schema, column names, data types
- Upload images (e.g., screenshot of an Alteryx formula) and ask Genie to replicate it
- Interactive chat history for iterative refinement

**Example prompts:**
- *"Categorize customers by age: Gen Z (<25), Millennial (25-39), Gen X (40-54), Boomer (55+)"*
- *"Calculate month-over-month revenue growth"*
- *"Find duplicate records based on email, keeping the most recent"*

**Alteryx has nothing comparable.**

---

# Feature: Join Operator

**Combine datasets with full control:**

- Join types: Inner, Left, Right, Full
- Multiple join conditions supported
- Output column selection (avoid duplicate columns)
- Add custom expression columns to joined results
- Chain multiple joins for multi-table workflows

**vs Alteryx:** Same Join tool concept, but custom expression columns in the join output is unique to Lakeflow Designer.

---

# Feature: Aggregate Operator

**10 built-in aggregation functions:**

`AVG` | `COUNT` | `MAX` | `MEAN` | `MEDIAN` | `MIN` | `PERCENTILE` | `STDDEV` | `SUM` | `VARIANCE`

- Multiple aggregations in a single operator
- Multiple grouping columns
- Group-by columns auto-included in output

**vs Alteryx:** The Summarize tool offers similar functions, but PERCENTILE, STDDEV, and VARIANCE require the R/Python tool in Alteryx. Here they're built-in.

---

# Feature: Combine Operator

**Three set operations in one:**

| Operation | Mode | Result |
|---|---|---|
| **Union** | All | Append all rows (including duplicates) |
| **Union** | Distinct | Append and deduplicate |
| **Intersect** | Distinct | Only rows present in both inputs |
| **Except** | Distinct | Rows in first input but NOT in second |

Requirement: both inputs must have matching schemas.

**vs Alteryx:** Replaces Union tool. Intersect and Except require workarounds in Alteryx (Join + Filter). Here they're one click.

---

# Feature: Pivot / Reshape

**Bidirectional reshaping:**

**Rows to Columns (Pivot)**
- Select pivot column (distinct values become headers)
- Choose value column and aggregation function
- Handle nulls and missing values

**Columns to Rows (Unpivot)**
- Select columns to unpivot
- Configure key and value column names

**vs Alteryx:** Replaces Cross Tab (pivot) and Transpose (unpivot) tools in a single, unified operator.

---

# Feature: SQL & Python Operators

### SQL Operator
- Write any `SELECT` statement
- Reference upstream operators by name as tables
- Window functions, CTEs, complex logic
- Great for analysts comfortable with SQL

### Python Operator
- Full PySpark environment
- Access inputs via `inputs["data"]`
- Assign result to `result` variable
- Distributed execution (not single-machine like Alteryx Python)

**vs Alteryx:** SQL operator is far more powerful than In-Database tools. Python runs on Spark, not limited to pandas on a single core.

---

# Feature: Output & Scheduling

### Output Operator
- Write results to Unity Catalog tables
- Governed, versioned, lineage-tracked
- One-click materialization

### Scheduling
- **Schedule button** for direct cron-based scheduling
- **Databricks Jobs** integration for multi-step orchestration
  - Combine visual pipelines with notebooks, SQL, ML tasks
  - Dependency management, retries, alerting

**vs Alteryx:** Replaces Alteryx Server ($$$) with built-in scheduling. Jobs orchestration is far more powerful than Alteryx Scheduler.

---

# Feature: Data Profiling & Preview

**Instant feedback at every step:**

- **Sample dataset** (1,000 rows) for fast iteration
- **Full dataset** for validation
- **Data profiling sidebar**: distributions, stats, null counts
- **Input/output comparison** view
- Click any operator to see its output immediately

**vs Alteryx:** No need to "Run" the entire workflow. Instant previews save significant iteration time.

---

# Canvas Navigation & Productivity

| Feature | Details |
|---|---|
| Pan | Space + drag |
| Zoom | Ctrl/Cmd + scroll |
| Auto-layout | One-click arrange operators |
| Fit view | Show all operators |
| Copy/Paste | Cmd/Ctrl + C/V for operators |
| Undo/Redo | Cmd/Ctrl + Z / Shift+Z |
| Right-click menu | Context actions |
| Drag-and-drop files | CSV/Excel auto-creates Source operator |

---

# Governance & Architecture

### Unity Catalog Native
- All sources and outputs are governed UC assets
- Column-level lineage tracked automatically
- Access controls (GRANT/REVOKE) apply to visual pipelines
- Data discovery through UC search

### Code-Backed
- Every visual transformation generates code
- Auditable, reproducible, version-controlled
- Can export to notebooks for advanced users

### Serverless
- No cluster management
- Pay only for compute used
- Instant start, auto-scale

---

# Alteryx vs Lakeflow Designer Summary

| Dimension | Alteryx | Lakeflow Designer |
|---|---|---|
| **Execution** | Single machine | Distributed (Spark serverless) |
| **Governance** | External / manual | Unity Catalog native |
| **AI assistance** | None | Genie Code (NL to code) |
| **Scheduling** | Alteryx Server ($$) | Built-in + Databricks Jobs |
| **Collaboration** | Gallery | Workspace sharing + Git |
| **Data sources** | ODBC/file drivers | UC tables, volumes, SaaS connectors |
| **Lineage** | None | Automatic column-level |
| **Scalability** | GB scale | TB+ scale |
| **Cost model** | Per-seat license | Consumption-based |
| **Code export** | Limited | Full Spark SQL / PySpark |

---

# Migration Path from Alteryx

### Phase 1: Quick Wins (Weeks 1-2)
- Identify top 10 most-used Alteryx workflows
- Rebuild them in Lakeflow Designer
- Compare execution time and results

### Phase 2: Team Onboarding (Weeks 3-4)
- Workshop: Lakeflow Designer hands-on lab (this deck!)
- Genie Code training for formula migration
- Set up shared catalog and schemas

### Phase 3: Production Migration (Months 2-3)
- Migrate remaining workflows
- Set up scheduling in Databricks Jobs
- Decommission Alteryx Server
- Monitor with Unity Catalog lineage

---

# Hands-On Lab Overview

**9 modules covering every feature:**

| Module | What You'll Build |
|---|---|
| 1. First Visual Data Prep | Canvas basics, source, preview |
| 2. Filtering & Sorting | Filter, Sort, Limit operators |
| 3. Transforms & Expressions | Custom columns, Genie Code AI |
| 4. Joins | Multi-table joins |
| 5. Aggregations | Grouping, functions |
| 6. Combine & Reshape | Union, Pivot, Unpivot |
| 7. SQL & Python | Custom code operators |
| 8. Output & Schedule | Write tables, automate |
| 9. End-to-End Pipeline | Complete Alteryx-replacement workflow |

**Dataset:** Retail supply chain (6 tables, 100K+ rows)

---

# Lab Dataset

```
customers (5K)  ---+
                   +--> orders (25K) --> order_items (75K)
stores (50)     ---+                        |
                                            v
                                     products (500)
suppliers (100)
```

Realistic French retail data:
- Customers with demographics and loyalty tiers
- Products across 5 categories with pricing
- Orders over 2 years via Web/Store/Mobile
- Suppliers with ratings and lead times

---

<!-- _class: lead -->

# Demo Time

### Let's build a pipeline together

---

# Next Steps

1. **Try the lab** -- run the data generation notebook and follow the guide
2. **Identify your top Alteryx workflows** -- we'll help you map them
3. **Workshop session** -- schedule a team onboarding with your SA
4. **Pilot project** -- pick one production workflow to migrate
5. **Review governance** -- compare UC lineage vs your current Alteryx audit

### Resources
- [Lakeflow Designer docs](https://docs.databricks.com/aws/en/designer/what-is-lakeflow-designer)
- [Lab repository](https://github.com/marionlamoureux/lakeflow_designer)

---

<!-- _class: lead -->

# Thank You
## Questions?
