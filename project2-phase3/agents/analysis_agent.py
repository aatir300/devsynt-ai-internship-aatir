import pandas as pd
from agents.state import PipelineState


def analysis_agent(state: PipelineState) -> PipelineState:
    """
    Generates key insights from the cleaned data, using whatever
    columns the Domain Config Agent identified as meaningful for
    this dataset's domain. Adapts what it calculates based on which
    columns actually exist, instead of assuming a fixed shape.
    """
    print("📊 Analysis Agent: starting...")

    try:
        df = state["cleaned_df"]
        config = state["domain_config"]

        if config is None:
            raise ValueError("No domain config available — cannot analyze without column mapping")

        revenue_col = config.get("revenue_column")
        qty_col = config.get("quantity_column")
        category_col = config.get("category_column")
        region_col = config.get("region_column")
        date_col = config.get("date_column")

        results = {
            "domain": config.get("domain", "unknown"),
            "total_rows": len(df),
        }

        # Revenue-based metrics (only if a revenue column exists)
        if revenue_col and revenue_col in df.columns:
            results["total_revenue"] = round(df[revenue_col].sum(), 2)
            results["avg_revenue"] = round(df[revenue_col].mean(), 2)
            results["revenue_label"] = revenue_col

        # Quantity-based metrics
        if qty_col and qty_col in df.columns:
            results["total_quantity"] = int(df[qty_col].sum())
            results["quantity_label"] = qty_col

        # Category breakdown (top groups by revenue, or by count if no revenue)
        if category_col and category_col in df.columns:
            if revenue_col and revenue_col in df.columns:
                by_category = (
                    df.groupby(category_col)[revenue_col]
                    .sum()
                    .sort_values(ascending=False)
                    .round(2)
                    .to_dict()
                )
            else:
                by_category = df[category_col].value_counts().to_dict()
            results["by_category"] = by_category
            results["category_label"] = category_col

        # Region breakdown
        if region_col and region_col in df.columns:
            if revenue_col and revenue_col in df.columns:
                by_region = (
                    df.groupby(region_col)[revenue_col]
                    .sum()
                    .sort_values(ascending=False)
                    .round(2)
                    .to_dict()
                )
            else:
                by_region = df[region_col].value_counts().to_dict()
            results["by_region"] = by_region
            results["region_label"] = region_col

        # Top 5 entries by revenue, using the category column as the label if available
        if revenue_col and revenue_col in df.columns:
            label_col = category_col if category_col in df.columns else df.columns[0]
            top_items = (
                df.groupby(label_col)[revenue_col]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .round(2)
                .to_dict()
            )
            results["top_items"] = top_items

        print(f"📊 Analysis Agent: done. Domain: {results['domain']}")
        print(f"📊 Results: {results}")

        state["analysis_results"] = results
        state["current_step"] = "analyzed"

    except Exception as e:
        print(f"⚠️ Analysis Agent failed: {e}")
        state["error"] = f"Analysis failed: {str(e)}"
        state["analysis_results"] = {"domain": "unknown", "total_rows": len(state.get("cleaned_df", []))}

    return state