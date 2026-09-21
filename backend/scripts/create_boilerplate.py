import os
from pathlib import Path

BACKEND_DIR = Path("D:/Downloads/datapilot-ai/backend")

# Create directories and __init__.py files
init_paths = [
    "app/__init__.py", "app/api/__init__.py", "app/api/routes/__init__.py", 
    "app/config/__init__.py", "app/schemas/__init__.py", "app/services/__init__.py",
    "app/services/ai/__init__.py", "app/services/analytics/__init__.py",
    "app/services/cleaning/__init__.py", "app/services/ingestion/__init__.py",
    "app/services/profiling/__init__.py", "app/services/forecasting/__init__.py",
    "app/services/anomaly_detection/__init__.py", "app/services/reporting/__init__.py",
    "app/services/billing/__init__.py", "app/services/email/__init__.py",
    "app/tasks/__init__.py", "app/prompts/__init__.py", "tests/__init__.py"
]

for p in init_paths:
    full_path = BACKEND_DIR / p
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.touch(exist_ok=True)

# Generate Prompt text files
prompts = {
    "insights.txt": "Analyze the metrics and generate actionable business insights.",
    "chat.txt": "Answer the user question strictly using the provided dataset context.",
    "dataset_classifier.txt": "Classify the dataset based on columns and samples.",
    "report_summary.txt": "Provide an executive summary of the analysis."
}

for name, content in prompts.items():
    (BACKEND_DIR / f"app/prompts/{name}").write_text(content)

print("Generated __init__.py and prompts successfully.")
