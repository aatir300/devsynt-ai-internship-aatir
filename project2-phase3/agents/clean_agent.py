import pandas as pd
from agents.state import PipelineState


def clean_agent(state: PipelineState) -> PipelineState:
    """
    Cleans the dataset using the column mapping from domain_config,
    instead of assuming fixed column names. Works across different
    dataset domains as long as the Domain Config Agent identified
    the relevant columns.
    """
    print("🧹 Clean Agent: starting...")

    try:
        if state.get("domain_config") is None:
            raise ValueError("No domain config available — cannot clean without column mapping")

        df = state["raw_df"].copy()
        config = state["domain_config"]
        notes = []
        initial_rows = len(df)

        revenue_col = config.get("revenue_column")
        qty_col = config.get("quantity_column")
        region_col = config.get("region_column")
        category_col = config.get("category_column")
        date_col = config.get("date_column")

        # Handle missing values, only for columns that actually exist in this dataset
        if revenue_col and revenue_col in df.columns:
            missing = df[revenue_col].isna().sum()
            df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce").fillna(0)
            notes.append(f"Filled {missing} missing '{revenue_col}' values with 0")

            # Fix negative revenue (doesn't make sense in any domain)
            broken = (df[revenue_col] < 0).sum()
            df.loc[df[revenue_col] < 0, revenue_col] = 0
            if broken:
                notes.append(f"Fixed {broken} rows with negative '{revenue_col}' values")

        if qty_col and qty_col in df.columns:
            missing = df[qty_col].isna().sum()
            df[qty_col] = pd.to_numeric(df[qty_col], errors="coerce").fillna(1)
            notes.append(f"Filled {missing} missing '{qty_col}' values with 1")

        if region_col and region_col in df.columns:
            missing = df[region_col].isna().sum()
            df[region_col] = df[region_col].fillna("Unknown")
            df[region_col] = df[region_col].astype(str).apply(lambda x: x if x.isupper() and len(x) <= 4 else x.title())
            notes.append(f"Filled {missing} missing '{region_col}' values with 'Unknown'")

        if category_col and category_col in df.columns:
            df[category_col] = df[category_col].astype(str).apply(lambda x: x if x.isupper() and len(x) <= 4 else x.title())
            notes.append(f"Standardized text formatting in '{category_col}'")

        if date_col and date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            notes.append(f"Converted '{date_col}' to proper date format")

        # Remove exact duplicate rows (applies regardless of domain)
        duplicates = df.duplicated().sum()
        df = df.drop_duplicates()
        notes.append(f"Removed {duplicates} duplicate rows")

        final_rows = len(df)
        notes.append(f"Final dataset: {final_rows} rows (started with {initial_rows})")

        cleaning_summary = "\n".join(f"- {note}" for note in notes)
        print(f"🧹 Clean Agent: done.\n{cleaning_summary}")

        state["cleaned_df"] = df
        state["cleaning_notes"] = cleaning_summary
        state["current_step"] = "cleaned"

    except Exception as e:
        print(f"⚠️ Clean Agent failed: {e}")
        state["error"] = f"Cleaning failed: {str(e)}"
        state["cleaned_df"] = state.get("raw_df")  # fall back to raw data so pipeline can continue
        state["cleaning_notes"] = f"Cleaning failed: {str(e)}"

    return state