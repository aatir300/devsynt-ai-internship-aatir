# Prompt Evolution Log — Project 2, Phase 3

This log documents real issues found while testing the pipeline across 5 different-domain datasets, and the fixes made in response.

---

## Test 1: `retail_sales.csv` (original Phase 2 dataset)
**Result:** ✅ Fully correct. Domain: "retail sales". All 6 columns mapped correctly.

## Test 2: `ecommerce_orders.csv`

**Issue found #1 — Domain label too generic**
The Domain Configuration Agent initially labeled this dataset as `"retail sales"` — not wrong, but not specific either, when the column names (`order_ref`, `buyer_country`) clearly pointed to e-commerce specifically.

**Fix:** Updated the domain-detection prompt to explicitly instruct the model to look closely at column names for domain-specific clues and prefer a more specific label over a generic one, rather than defaulting to the first plausible category.

**Result after fix:** Domain correctly relabeled as `"e-commerce sales"`.

---

**Issue found #2 — Acronyms getting mangled by text cleaning**
The Clean Agent's text-standardization step used `.str.title()` on every region/category value. This turned `"UK"` into `"Uk"` and `"USA"` into `"Usa"` — technically "clean" formatting, but factually wrong for acronyms.

**Fix:** Changed the cleaning logic to check whether a value is already fully uppercase and short (4 characters or fewer) before title-casing it — if so, leave it untouched, since it's likely an acronym or country code.

**Result after fix:** `"UK"` and `"USA"` preserved correctly.

---

## Test 3: `inventory_stock.csv` (deliberately has no revenue column)

**Result:** ✅ No crash. The pipeline correctly detected `revenue_column: null`, and every downstream agent — Analysis and Dashboard — simply skipped all revenue-based calculations and stat cards instead of erroring or displaying fake $0.00 values. The dashboard rendered with 2 stat cards and 2 charts instead of 4 and 3, appropriately.

**Observation (not fixed, documented as a known limitation):**
Missing `stock_count` values were filled with `1`, using the same generic rule as "missing order quantity → assume 1." For inventory data specifically, this is a weaker assumption — a missing stock count more plausibly means "unknown" than "exactly one unit in stock." We chose to document this rather than build domain-specific fill logic, since the beginner-level scope of this phase doesn't call for a full rules engine per domain — but it's a genuine limitation worth being transparent about.

## Test 4: `restaurant_sales.csv`

**Result:** ✅ Fully correct on first run, no issues. Domain correctly labeled "restaurant dining"; all 6 columns mapped correctly (`bill_amount` → revenue, `dish_category` → category, `table_section` → region).

## Test 5: `saas_subscriptions.csv`

**Result:** ✅ Ran successfully across all 4 agents with no crashes.

---

## Summary of changes made

| Change | Reason |
|---|---|
| Domain-detection prompt updated to require specific, column-informed labels | "retail sales" was too generic for e-commerce data |
| Text-cleaning logic updated to preserve short all-caps acronyms | `.str.title()` was breaking "UK"/"USA" into "Uk"/"Usa" |

## What this testing round confirmed

The pipeline's core design — driving every agent off a dynamically detected `domain_config` instead of hardcoded column names — held up across 5 structurally different datasets, including one with a completely missing revenue column. The two real issues found were both in the **generic text-cleaning and labeling logic**, not in the core architecture, which is a good sign the underlying multi-agent design is sound.
