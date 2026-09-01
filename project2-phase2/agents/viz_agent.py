import matplotlib
matplotlib.use("Agg")  # no GUI needed, just save files
import matplotlib.pyplot as plt
from agents.state import PipelineState


def viz_agent(state: PipelineState) -> PipelineState:
    """
    Generates simple charts from the analysis results and saves them
    as images for the dashboard.
    """
    print("📈 Visualization Agent: starting...")
    results = state["analysis_results"]

    # Chart 1: Sales by Category (bar chart)
    categories = list(results["sales_by_category"].keys())
    cat_sales = list(results["sales_by_category"].values())

    plt.figure(figsize=(7, 5))
    plt.bar(categories, cat_sales, color="#5fc9c0")
    plt.title("Total Sales by Category")
    plt.ylabel("Sales ($)")
    plt.xlabel("Category")
    plt.tight_layout()
    plt.savefig("assets/chart-sales-by-category.png")
    plt.close()
    print("📈 Saved chart-sales-by-category.png")

    # Chart 2: Top 5 Products (bar chart)
    products = list(results["top_products"].keys())
    product_sales = list(results["top_products"].values())

    plt.figure(figsize=(7, 5))
    plt.barh(products, product_sales, color="#f2a65a")
    plt.title("Top 5 Best-Selling Products")
    plt.xlabel("Sales ($)")
    plt.gca().invert_yaxis()  # highest value at the top
    plt.tight_layout()
    plt.savefig("assets/chart-top-products.png")
    plt.close()
    print("📈 Saved chart-top-products.png")

    # Chart 3: Sales by Region (pie chart)
    regions = list(results["sales_by_region"].keys())
    region_sales = list(results["sales_by_region"].values())

    plt.figure(figsize=(6, 6))
    plt.pie(region_sales, labels=regions, autopct="%1.1f%%",
            colors=["#5fc9c0", "#f2a65a", "#e1654a", "#9fb3d1", "#122a4e"])
    plt.title("Sales Share by Region")
    plt.tight_layout()
    plt.savefig("assets/chart-sales-by-region.png")
    plt.close()
    print("📈 Saved chart-sales-by-region.png")

    state["current_step"] = "visualized"
    print("📈 Visualization Agent: done.")
    return state