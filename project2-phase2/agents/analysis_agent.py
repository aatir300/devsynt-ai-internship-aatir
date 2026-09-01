import pandas as pd
from agents.state import PipelineState


def analysis_agent(state: PipelineState) -> PipelineState:
    """
    Generates key business insights from the cleaned retail data.
    """
    print("📊 Analysis Agent: starting...")
    df = state["cleaned_df"]
    
    total_sales = round(df["sales"].sum(), 2)
    total_orders = len(df)
    total_quantity = int(df["quantity"].sum())
    avg_order_value = round(df["sales"].mean(), 2)

    # Best-selling products (by total sales)
    top_products = (
        df.groupby("product")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .round(2)
        .to_dict()
    )

    # Sales by category
    sales_by_category = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
        .to_dict()
    )

    # Sales by region
    sales_by_region = (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
        .to_dict()
    )
    
    results = {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "avg_order_value": avg_order_value,
        "top_products": top_products,
        "sales_by_category": sales_by_category,
        "sales_by_region": sales_by_region,
    }

    print("📊 Analysis Agent: done.")
    print(f"Total Sales: ${total_sales:,.2f}")
    print(f"Total Orders: {total_orders}")
    print(f"Top Product: {list(top_products.keys())[0]}")

    state["analysis_results"] = results
    state["current_step"] = "analyzed"
    return state