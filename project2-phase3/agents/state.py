from typing import TypedDict, Optional
import pandas as pd


class PipelineState(TypedDict):
    """
    Shared state that flows through the graph.
    Unlike Phase 2, this state doesn't assume fixed column names —
    domain_config holds whatever column mapping was detected for THIS dataset.
    """
    raw_data_path: str
    raw_df: Optional[pd.DataFrame]
    domain_config: Optional[dict]        # NEW: detected domain + column mapping
    cleaned_df: Optional[pd.DataFrame]
    cleaning_notes: Optional[str]
    analysis_results: Optional[dict]
    dashboard_html: Optional[str]        # NEW: the Dashboard Agent's generated output
    error: Optional[str]                 # NEW: for graceful error handling
    current_step: str