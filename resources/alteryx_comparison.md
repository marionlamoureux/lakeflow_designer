# Alteryx vs Lakeflow Designer - Detailed Comparison

## Executive Summary

Lakeflow Designer replaces Alteryx for visual data preparation with three key advantages:
1. **Governance by default** -- Unity Catalog integration means lineage, access control, and audit from day one.
2. **Scalability** -- runs on Spark serverless, not a single machine; handles TB-scale data.
3. **AI-assisted development** -- Genie Code generates expressions from natural language, accelerating analyst productivity.

---

## Tool-by-Tool Mapping

### Data Input/Output

| Alteryx | Lakeflow Designer | Notes |
|---|---|---|
| Input Data (file) | Source operator (drag-drop CSV/Excel) | No file path management; files uploaded to workspace |
| Input Data (database) | Source operator (UC table) | No ODBC drivers; governed access via Unity Catalog |
| Connect In-DB | Source operator (UC table) | All tables are lakehouse-native |
| Output Data | Output operator | Writes to UC tables; instantly queryable |
| Directory | Source from UC Volume | Browse volumes in Unity Catalog |
| Download | Not needed | Data stays in the lakehouse |

### Data Preparation

| Alteryx | Lakeflow Designer | Notes |
|---|---|---|
| Select | Transform (checkboxes) | Select, rename, reorder in one operator |
| Auto Field | Not needed | Schema inferred automatically |
| Data Cleansing | Transform + Genie Code | Prompt: "trim whitespace, handle nulls" |
| Filter | Filter operator | Graphical condition builder |
| Sort | Sort operator | Multi-column, ASC/DESC |
| Sample | Limit operator | Also: sample toggle in preview |
| Unique | Combine (Distinct) or SQL | `SELECT DISTINCT` via SQL operator |
| Formula | Transform > Custom column | Expression editor + Genie AI |
| Multi-Row Formula | SQL operator (window functions) | `LAG`, `LEAD`, `ROW_NUMBER`, etc. |
| Multi-Field Formula | Transform > multiple custom columns | Or Genie: "apply X to all numeric columns" |
| Record ID | Transform > Custom column | Expression: `monotonically_increasing_id()` |
| Running Total | SQL operator (window) | `SUM() OVER (ORDER BY ...)` |

### Join & Combine

| Alteryx | Lakeflow Designer | Notes |
|---|---|---|
| Join | Join operator | Inner, Left, Right, Full |
| Find Replace | Join + Transform | Left join + COALESCE expression |
| Append Fields | Join (cross join via SQL) | SQL: `SELECT * FROM a CROSS JOIN b` |
| Union | Combine (Union) | All or Distinct mode |
| Make Group | Not applicable | Use Group By in Aggregate |

### Analytics & Reshaping

| Alteryx | Lakeflow Designer | Notes |
|---|---|---|
| Summarize | Aggregate operator | 10 built-in functions |
| Cross Tab | Pivot (Rows to Columns) | Unified Pivot operator |
| Transpose | Pivot (Columns to Rows) | Same operator, toggle mode |
| Running Total | SQL window function | More flexible than Alteryx |
| Weighted Average | Transform + Aggregate | Custom expression for weighted calc |
| Percentile | Aggregate (PERCENTILE) | Built-in; requires R tool in Alteryx |

### Spatial (not available in Designer)

Alteryx spatial tools (Buffer, Distance, Spatial Match, Trade Area) do not have direct equivalents in Lakeflow Designer. For spatial analysis, use Databricks notebooks with H3 or Mosaic libraries, then bring the result tables into Designer.

### Reporting

| Alteryx | Lakeflow Designer | Notes |
|---|---|---|
| Browse | Output pane + Data Profiling | Live at every step, no run needed |
| Table | Output to UC > AI/BI Dashboard | Build dashboards on output tables |
| Chart | Data Profiling sidebar | Distributions and stats |
| Report | Not applicable | Use AI/BI Dashboards or notebooks |

### Developer

| Alteryx | Lakeflow Designer | Notes |
|---|---|---|
| Python tool | Python operator | PySpark (distributed) |
| R tool | Not available | Use notebooks for R |
| Command | Not available | Use Databricks Jobs |
| Dynamic Input | Parameterized via SQL operator | Or Python operator |

### Automation

| Alteryx | Lakeflow Designer | Notes |
|---|---|---|
| Scheduler | Schedule button | Cron-based, built-in |
| Alteryx Server | Databricks Jobs | Multi-step orchestration, monitoring, alerting |
| Alteryx Gallery | Workspace sharing | Role-based access, Git integration |
| Alteryx Analytics Hub | Unity Catalog | Centralized governance |

---

## What Lakeflow Designer Does Better

1. **Instant preview at every step** -- no need to run the full workflow to see intermediate results
2. **AI code generation** -- describe a transformation in English, get the expression
3. **Governed by default** -- Unity Catalog lineage, access controls, audit logs
4. **Serverless execution** -- no machine sizing, no bottlenecks, auto-scales
5. **Code export** -- visual pipelines generate Spark SQL/PySpark that advanced users can extend
6. **Cost efficiency** -- consumption-based pricing vs per-seat licensing
7. **Platform integration** -- part of Databricks, alongside ML, BI, and data engineering tools

## What Alteryx Still Does (That Designer Doesn't Yet)

1. **Spatial analytics** -- Alteryx has rich spatial tools; use Databricks Mosaic/H3 for spatial work
2. **Predictive/statistical tools** -- Alteryx has built-in ML blocks; use Databricks ML for this
3. **Reporting/render** -- Alteryx can generate formatted PDF reports; use AI/BI Dashboards
4. **Macro system** -- Alteryx macros allow reusable workflow components; use parameterized notebooks
5. **Desktop experience** -- Alteryx runs locally; Lakeflow Designer is browser-based (cloud-first)
