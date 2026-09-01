# Project 2 — Phase 2: Multi-Agent Retail Data Pipeline

A LangGraph-orchestrated multi-agent pipeline that takes a raw, messy retail sales CSV and turns it into cleaned data, business insights, and a visual dashboard — no manual steps in between.

## The Dataset

A retail sales dataset (`data/retail_sales_raw.csv`) with 608 rows covering orders across three categories (Furniture, Technology, Office Supplies), four regions, and the full 2024 calendar year. Columns: `order_id, date, product, category, region, quantity, sales`.

The raw file was deliberately messy — missing values, a few broken negative sales figures, inconsistent text casing, and duplicate rows — to give the Clean Agent real work to do, similar to what a genuine raw export would look like.

## The Pipeline, Step by Step

### 1. Orchestrator Agent (`agents/orchestrator.py`)

Built with LangGraph's `StateGraph`. This is the "manager" — it doesn't clean or analyze anything itself, it just defines the graph: which agent (node) runs first, and what happens next (edge). The routing is:

```
clean → analyze → visualize → end
```

A shared `PipelineState` (defined in `agents/state.py`) flows through every node — each agent reads what it needs from state and writes its results back before passing it to the next node. This is the node → edge → state pattern from Phase 1.

See `assets/flow-diagram.png` — an auto-generated diagram of the actual graph structure (not hand-drawn — LangGraph draws its own graph from the real code).

### 2. Clean Agent (`agents/clean_agent.py`)

Takes the raw data and fixes it:
- Filled missing `sales` values with 0, missing `quantity` with 1, missing `region` with "Unknown"
- Fixed 2 rows with impossible negative sales values (treated as 0)
- Standardized inconsistent text capitalization (e.g. "office chair" → "Office Chair")
- Removed 8 exact duplicate rows
- Corrected data types (quantity as integer, sales as float, date as an actual date type)

Result: 608 raw rows → 600 cleaned rows. Full before/after proof: `assets/cleaning-result.png`.

### 3. Analysis (EDA) Agent (`agents/analysis_agent.py`)

Takes the cleaned data and calculates real business insights:
- **Total sales:** $856,027.18 across 600 orders
- **Average order value:** $1,426.71
- **Top 5 best-selling products** by revenue
- **Sales broken down by category** and **by region**

Proof of output: `assets/analysis-output.png`.

### 4. Visualization Agent — Bonus (`agents/viz_agent.py`)

Turns the analysis results into three charts, saved to `assets/`:
- `chart-sales-by-category.png` — bar chart
- `chart-top-products.png` — horizontal bar chart of the top 5 products
- `chart-sales-by-region.png` — pie chart of regional sales share

### 5. Dashboard (`dashboard/dashboard.html` + `dashboard.css`)

A static HTML page presenting the final results: key numbers up top (total sales, orders, units sold, average order value), the three charts from the Visualization agent, and the Clean Agent's notes at the bottom for transparency about what was fixed. Screenshot: `assets/dashboard-preview.png`.

## How to Run It

```bash
cd project2-phase2
python -m venv venv
venv\Scripts\activate          # Windows
pip install langchain langgraph langchain-google-genai pandas matplotlib python-dotenv
python -m agents.orchestrator
```

This runs the full pipeline (clean → analyze → visualize) and regenerates everything in `assets/`. Then open `dashboard/dashboard.html` in any browser to view the results.

**Note on credentials:** a `.env` file holding a `GOOGLE_API_KEY` is expected by the project setup but is not committed to this repo (see `.gitignore`). To run any LLM-dependent extensions, add your own Gemini API key there.

## What I Learned Building This

The biggest shift from Phase 1's theory to this build was actually thinking in **shared state** rather than passing separate variables between functions — every agent reads from and writes to the same `PipelineState` dictionary, which is what makes it possible for LangGraph to chain them together generically instead of hardcoding "run function A, take its output, pass it to function B." Debugging the environment (a broken virtual environment installing packages into the wrong place) was its own lesson in double-checking that tools are actually pointing where you think they are, not just trusting that a command "worked" because it didn't show an error.
