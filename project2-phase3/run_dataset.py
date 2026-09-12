import sys
from agents.orchestrator import run_pipeline

if __name__ == "__main__":
    csv_path = sys.argv[1]
    result = run_pipeline(csv_path)