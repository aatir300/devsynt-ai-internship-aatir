import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.state import PipelineState

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)


def domain_config_agent(state: PipelineState) -> PipelineState:
    """
    Looks at the incoming dataset's structure and figures out:
    - what domain/type of data this is
    - which columns serve which purpose (revenue, category, date, etc.)
    This config is then used by every downstream agent instead of
    hardcoded column names.
    """
    print("🔍 Domain Config Agent: starting...")

    try:
        df = state["raw_df"]
        columns = list(df.columns)
        sample_rows = df.head(3).to_dict(orient="records")

        prompt = f"""You are a data analyst. Look at this dataset's columns and sample rows,
and identify what business domain it represents and which columns serve which purpose.

Columns: {columns}
Sample rows: {json.dumps(sample_rows, default=str)}

Respond ONLY with valid JSON in this exact structure, no other text:
{{
  "domain": "a short label like 'retail sales' or 'saas subscriptions' or 'inventory stock'",
  "revenue_column": "the column name that represents money/revenue/sales, or null if none exists",
  "quantity_column": "the column name representing quantity/count/units, or null if none exists",
  "category_column": "the column name representing a grouping/category, or null if none exists",
  "date_column": "the column name representing a date, or null if none exists",
  "region_column": "the column name representing region/location, or null if none exists",
  "id_column": "the column name that looks like a unique identifier, or null if none exists"
}}"""

        response = llm.invoke(prompt)

        if isinstance(response.content, list):
            raw_text = "".join(
                part if isinstance(part, str) else part.get("text", "")
                for part in response.content
            ).strip()
        else:
            raw_text = response.content.strip()

        # Remove markdown code fences if the model adds them anyway
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`").replace("json", "", 1).strip()

        config = json.loads(raw_text)

        print(f"🔍 Domain detected: {config['domain']}")
        print(f"🔍 Column mapping: {config}")

        state["domain_config"] = config
        state["current_step"] = "domain_configured"

    except Exception as e:
        print(f"⚠️ Domain Config Agent failed: {e}")
        state["error"] = f"Domain configuration failed: {str(e)}"
        state["domain_config"] = None

    return state