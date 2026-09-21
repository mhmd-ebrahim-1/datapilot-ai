import uuid
import logging
from app.tasks.celery_app import celery_app
from app.config.database import SessionLocal
from app.services.reporting.report_generator import create_report_for_dataset

logger = logging.getLogger("datapilot.tasks.report")

@celery_app.task
def generate_report_task(dataset_id: str, user_id: str, title: str = "Executive Report"):
    db = SessionLocal()
    try:
        report = create_report_for_dataset(
            db=db,
            dataset_id=uuid.UUID(dataset_id),
            user_id=uuid.UUID(user_id),
            title=title
        )
        logger.info(f"Generated report {report.id} for dataset {dataset_id}")
        return str(report.id)
    except Exception as e:
        logger.error(f"Failed to generate report for dataset {dataset_id}: {e}")
        raise
    finally:
        db.close()

