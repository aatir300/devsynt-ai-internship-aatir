from langgraph.graph import StateGraph, END
from agents.state import PipelineState
from agents.clean_agent import clean_agent
from agents.analysis_agent import analysis_agent
from agents.viz_agent import viz_agent


def build_pipeline():
    """
    Builds the LangGraph orchestrator: a graph that routes
    raw data through the Clean agent, then the Analysis agent.
    """
    graph = StateGraph(PipelineState)

    # Register each agent as a node
    graph.add_node("clean", clean_agent)
    graph.add_node("analyze", analysis_agent)
    graph.add_node("visualize", viz_agent)

    # Define the routing: where the graph starts, and what follows what
    graph.set_entry_point("clean")
    graph.add_edge("clean", "analyze")
    graph.add_edge("analyze", "visualize")
    graph.add_edge("visualize", END)

    # Compile into a runnable pipeline
    pipeline = graph.compile()
    return pipeline


def run_pipeline(csv_path: str) -> PipelineState:
    """
    Runs the full pipeline on a given CSV file path and returns
    the final state, containing cleaned data and analysis results.
    """
    import pandas as pd

    print(f"🚀 Orchestrator: loading raw data from {csv_path}")
    raw_df = pd.read_csv(csv_path)

    initial_state: PipelineState = {
        "raw_data_path": csv_path,
        "raw_df": raw_df,
        "cleaned_df": None,
        "cleaning_notes": None,
        "analysis_results": None,
        "current_step": "start",
    }

    pipeline = build_pipeline()
    final_state = pipeline.invoke(initial_state)

    print("🚀 Orchestrator: pipeline complete.")
    return final_state


if __name__ == "__main__":
    result = run_pipeline("data/retail_sales_raw.csv")
    print("\n--- Final State Summary ---")
    print(f"Current step: {result['current_step']}")
    print(f"Cleaned rows: {len(result['cleaned_df'])}")
    print(f"Total sales: ${result['analysis_results']['total_sales']:,.2f}")
        # Generate a visual diagram of the graph structure
    pipeline = build_pipeline()
    graph_image = pipeline.get_graph().draw_mermaid_png()
    with open("assets/flow-diagram.png", "wb") as f:
        f.write(graph_image)
    print("📈 Flow diagram saved to assets/flow-diagram.png")