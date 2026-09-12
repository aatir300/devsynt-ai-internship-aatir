from langgraph.graph import StateGraph, END
from agents.state import PipelineState
from agents.domain_config_agent import domain_config_agent
from agents.clean_agent import clean_agent
from agents.analysis_agent import analysis_agent
from agents.dashboard_agent import dashboard_agent


def build_pipeline():
    """
    Builds the LangGraph orchestrator: domain_config -> clean -> analyze -> dashboard.
    The domain_config step runs first so every later agent knows which
    columns matter for THIS specific dataset.
    """
    graph = StateGraph(PipelineState)

    graph.add_node("domain_config", domain_config_agent)
    graph.add_node("clean", clean_agent)
    graph.add_node("analyze", analysis_agent)
    graph.add_node("dashboard", dashboard_agent)

    graph.set_entry_point("domain_config")
    graph.add_edge("domain_config", "clean")
    graph.add_edge("clean", "analyze")
    graph.add_edge("analyze", "dashboard")
    graph.add_edge("dashboard", END)

    return graph.compile()


def run_pipeline(csv_path: str) -> PipelineState:
    """
    Runs the full pipeline on any CSV file and returns the final state.
    """
    import pandas as pd

    print(f"🚀 Orchestrator: loading raw data from {csv_path}")
    raw_df = pd.read_csv(csv_path)

    initial_state: PipelineState = {
        "raw_data_path": csv_path,
        "raw_df": raw_df,
        "domain_config": None,
        "cleaned_df": None,
        "cleaning_notes": None,
        "analysis_results": None,
        "dashboard_html": None,
        "error": None,
        "current_step": "start",
    }

    pipeline = build_pipeline()
    final_state = pipeline.invoke(initial_state)

    print("🚀 Orchestrator: pipeline complete.")
    if final_state.get("error"):
        print(f"⚠️ Pipeline completed with a warning: {final_state['error']}")
    return final_state


if __name__ == "__main__":
    result = run_pipeline("test-datasets/retail_sales.csv")

    # Save a visual diagram of the graph structure
    pipeline = build_pipeline()
    graph_image = pipeline.get_graph().draw_mermaid_png()
    with open("assets/flow-diagram.png", "wb") as f:
        f.write(graph_image)
    print("📈 Flow diagram saved to assets/flow-diagram.png")