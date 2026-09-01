import pandas as pd
from agents.state import PipelineState


def clean_agent(state: PipelineState) -> PipelineState:
    """
    Cleans the raw retail dataset:
    - fixes missing values
    - removes duplicate rows
    - fixes obviously broken data (like negative sales)
    - standardizes text formatting
    """
    print("🧹 Clean Agent: starting...")
    df = state["raw_df"].copy()
    notes = []

    initial_rows = len(df)

    # Missing sales -> fill with 0 (can't guess a real sales figure)
    missing_sales = df["sales"].isna().sum()
    df["sales"] = df["sales"].fillna(0)

    # Missing quantity -> fill with 1 (safest assumption for a single order)
    missing_qty = df["quantity"].isna().sum()
    df["quantity"] = df["quantity"].fillna(1)

    # Missing region -> fill with "Unknown"
    missing_region = df["region"].isna().sum()
    df["region"] = df["region"].fillna("Unknown")

    notes.append(f"Filled {missing_sales} missing sales values with 0")
    notes.append(f"Filled {missing_qty} missing quantity values with 1")
    notes.append(f"Filled {missing_region} missing region values with 'Unknown'")

    # Fix broken data: negative sales don't make sense, treat as 0
    broken_sales = (df["sales"] < 0).sum()
    df.loc[df["sales"] < 0, "sales"] = 0
    notes.append(f"Fixed {broken_sales} rows with negative sales values")

    # Standardize text formatting (e.g. "office chair" -> "Office Chair")
    df["product"] = df["product"].str.title()
    df["category"] = df["category"].str.title()
    df["region"] = df["region"].str.title()

    # Remove exact duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()
    notes.append(f"Removed {duplicates} duplicate rows")

    # Ensure correct data types
    df["quantity"] = df["quantity"].astype(int)
    df["sales"] = df["sales"].astype(float)
    df["date"] = pd.to_datetime(df["date"])

    final_rows = len(df)
    notes.append(f"Final dataset: {final_rows} rows (started with {initial_rows})")

    cleaning_summary = "\n".join(f"- {note}" for note in notes)
    print(f"🧹 Clean Agent: done.\n{cleaning_summary}")

    state["cleaned_df"] = df
    state["cleaning_notes"] = cleaning_summary
    state["current_step"] = "cleaned"
    return state