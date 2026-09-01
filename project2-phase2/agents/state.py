from typing import TypedDict, Optional
import pandas as pd


class PipelineState(TypedDict):
    """
    Shared state that flows through the graph.
    Each agent reads from this and updates it before passing it to the next agent.
    """
    raw_data_path: str          # path to the raw CSV file
    raw_df: Optional[pd.DataFrame]      # the raw data, once loaded
    cleaned_df: Optional[pd.DataFrame]  # the data after the Clean agent runs
    cleaning_notes: Optional[str]       # summary of what the Clean agent fixed
    analysis_results: Optional[dict]    # insights from the Analysis agent
    current_step: str            # tracks which agent is currently running