import pandas as pd
from agents.domain_config_agent import domain_config_agent
from agents.clean_agent import clean_agent
from agents.analysis_agent import analysis_agent

df = pd.read_csv("test-datasets/retail_sales.csv")

state = {
    "raw_data_path": "test-datasets/retail_sales.csv",
    "raw_df": df,
    "domain_config": None,
    "cleaned_df": None,
    "cleaning_notes": None,
    "analysis_results": None,
    "dashboard_html": None,
    "error": None,
    "current_step": "start"
}

state = domain_config_agent(state)
state = clean_agent(state)
state = analysis_agent(state)

print("\n--- Analysis Results ---")
for k, v in state["analysis_results"].items():
    print(f"{k}: {v}")