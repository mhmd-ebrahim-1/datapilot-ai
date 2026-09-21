import os
from pathlib import Path

BACKEND_DIR = Path("D:/Downloads/datapilot-ai/backend")

# Create missing simple services
services = {
    "app/services/billing/plans.py": "# Plans configuration",
    "app/services/billing/usage_service.py": "# Usage tracking logic",
    "app/services/billing/billing_service.py": "# Mock billing service",
    "app/services/email/email_service.py": "# Console email logic",
    "app/services/reporting/report_generator.py": "# Report generator logic",
    "app/services/notification_service.py": "# Simple notification service",
    "app/services/ai/validator.py": "# AI validation logic",
    "app/tasks/report_tasks.py": "# Report tasks logic"
}

for path, content in services.items():
    full_path = BACKEND_DIR / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if not full_path.exists():
        full_path.write_text(content)

print("Generated remaining simple service files.")
