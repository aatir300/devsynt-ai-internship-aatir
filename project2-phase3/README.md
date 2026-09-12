# Project 2 — Phase 3: Production-Grade Multi-Agent Data Pipeline

A LangGraph-orchestrated pipeline that takes **any** business CSV — regardless of domain or column naming — and automatically detects what it represents, cleans it, analyzes it, and generates a matching dashboard. Built as the final phase of a three-part project: Phase 1 covered LangChain/LangGraph fundamentals, Phase 2 built a working prototype on one fixed dataset, and this phase turns that prototype into a system that generalizes.

## Why This Phase Is Different From Phase 2

Phase 2's pipeline only worked because every agent had hardcoded column names (`df["sales"]`, `df["region"]`) written for one specific dataset shape. That's a demo, not a product — it breaks the moment you hand it a dataset with different column names. Phase 3 removes every hardcoded assumption and replaces it with a new agent that reasons about the data first.

## Architecture

```
raw CSV
   │
   ▼
┌─────────────────────┐
│ Domain Config Agent  │  ← NEW. Uses an LLM to read column names + sample
│                      │     rows and figure out: what domain is this, and
└──────────┬───────────┘     which column maps to revenue/category/region/etc.
           │
           ▼
┌─────────────────────┐
│    Clean Agent       │  ← Uses the detected column mapping instead of
│                      │     fixed names. Skips any cleaning step for a
└──────────┬───────────┘     column that doesn't exist in this dataset.
           │
           ▼
┌─────────────────────┐
│   Analysis Agent     │  ← Calculates totals/breakdowns only for whatever
│                      │     columns the domain config actually identified.
└──────────┬───────────┘
           │
           ▼
┌─────────────────────┐
│  Dashboard Agent     │  ← NEW. Builds the HTML dashboard's stat cards and
│                      │     charts dynamically — a dataset with no revenue
└──────────────────────┘     column simply gets fewer stat cards, not an error.
```

See `assets/flow-diagram.png` for the auto-generated LangGraph diagram of the actual compiled graph.

Every agent reads from and writes to one shared `PipelineState` object (`agents/state.py`) — this is what makes the graph-based design work: no agent needs to know how any other agent works internally, they just agree on a shared data shape.

## The Domain Configuration Agent, In Detail

This is the core new piece. Instead of assuming what a dataset looks like, it sends the LLM the actual column names and a few sample rows, and asks it to return structured JSON identifying: the domain label, and which column (if any) represents revenue, quantity, category, date, region, and a unique ID. Every other agent then reads from this config rather than assuming fixed names — so the same Clean Agent code that fills missing values in a `sales` column also correctly fills missing values in an `order_value`, `bill_amount`, or `mrr` column, without any per-dataset code changes.

## Error Handling

Every agent is wrapped in a try/except block. If an agent fails — a malformed dataset, an API hiccup, unexpected data — the pipeline doesn't crash. It records the error in shared state and continues with the best available fallback (e.g. the Clean Agent falls back to the raw, unfiltered data rather than stopping the whole pipeline). Any recorded error is also surfaced directly on the final dashboard as a visible warning banner, rather than failing silently.

## Testing Across 5 Different Domains

The pipeline was run end-to-end on 5 structurally different datasets, with no per-dataset code changes:

| # | Dataset | Domain Detected | Columns (raw → mapped) | Result |
|---|---|---|---|---|
| 1 | `retail_sales.csv` | retail sales | sales→revenue, category, region | ✅ `assets/dataset1-result.png` |
| 2 | `ecommerce_orders.csv` | e-commerce sales | order_value→revenue, item_type→category, buyer_country→region | ✅ `assets/dataset2-result.png` |
| 3 | `inventory_stock.csv` | inventory stock | *(no revenue column)*, stock_count→quantity, warehouse_location→region | ✅ `assets/dataset3-result.png` |
| 4 | `restaurant_sales.csv` | restaurant dining | bill_amount→revenue, dish_category→category, table_section→region | ✅ `assets/dataset4-result.png` |
| 5 | `saas_subscriptions.csv` | saas subscriptions | mrr→revenue, plan_tier→category, customer_region→region | ✅ `assets/dataset5-result.png` |

Dataset 3 (inventory) is the most important test: it has **no revenue-equivalent column at all**. The pipeline correctly detected this, and both the Analysis Agent and Dashboard Agent adapted by simply omitting every revenue-based metric and chart, rather than crashing or showing meaningless zeros.

## How the Prompts Evolved

Full details in `assets/prompt-evolution-log.md`. Summary of real issues found and fixed during testing:

1. **Domain labels were too generic** on first pass (e.g. "retail sales" for an e-commerce dataset). Fixed by updating the detection prompt to require the model to reason from specific column names rather than defaulting to the broadest plausible label.
2. **Acronyms were getting corrupted by text cleaning** — `.str.title()` turned "UK" into "Uk". Fixed by checking for short, all-uppercase values before applying title-casing.

One limitation was deliberately left undocumented-as-fixed rather than papered over: filling missing inventory stock counts with `1` (borrowed from the "missing order quantity" rule) is a weaker assumption for inventory data specifically. This is noted honestly in the evolution log rather than hidden.

## Project Structure

```
project2-phase3/
├── agents/
│   ├── state.py              shared state definition
│   ├── domain_config_agent.py   NEW — detects domain + column mapping
│   ├── clean_agent.py           domain-aware cleaning
│   ├── analysis_agent.py        domain-aware analysis
│   ├── dashboard_agent.py       NEW — generates dashboard dynamically
│   └── orchestrator.py          LangGraph graph definition
├── test-datasets/             all 5 datasets used in testing
├── assets/                    flow diagram + all result screenshots + evolution log
├── dashboard/                  generated dashboards + shared CSS
└── README.md
```

## How to Run It

```bash
cd project2-phase3
python -m venv venv
venv\Scripts\activate
pip install langchain langgraph langchain-google-genai pandas matplotlib python-dotenv
python run_dataset.py test-datasets/retail_sales.csv
```

Replace the CSV path with any dataset to run the full pipeline on it — no code changes needed per dataset. Output dashboard is saved to `dashboard/{dataset_name}-dashboard.html`.

**Credentials:** a `.env` file with `GOOGLE_API_KEY=your_key` is required (not committed — see `.gitignore`).

## What Changed My Thinking, Building This

Phase 2 taught me the mechanics of LangGraph. Phase 3 taught me the actual point of it: a graph only earns its complexity when the *steps themselves* need to adapt to different situations, not just run in a fixed order. The Domain Configuration Agent is doing real reasoning work an if/else chain couldn't — it has to generalize to data it's never seen, which is exactly the kind of judgment call that benefits from an LLM instead of hardcoded rules. The honest limitation I found (the inventory fill-value assumption) was a useful reminder that "production-grade" doesn't mean "handles every case perfectly" — it means the system fails predictably, reports what it doesn't know, and is honest about its own edges.
