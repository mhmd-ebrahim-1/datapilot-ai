from app.tasks.celery_app import celery_app
from app.config.database import SessionLocal
from app.models.dataset import Dataset
from app.services.ingestion.parser import parse_file
from app.services.ingestion.storage import get_file_path
from app.services.cleaning.cleaner import clean_dataset
from app.services.profiling.profiler import profile_dataframe
from app.services.profiling.quality_scorer import calculate_quality_score
from app.services.profiling.type_detector import detect_type
import uuid

@celery_app.task
def process_dataset_task(dataset_id: str):
    db = SessionLocal()
    try:
        dataset = db.query(Dataset).filter(Dataset.id == uuid.UUID(dataset_id)).first()
        if not dataset: return
        
        dataset.status = "processing"
        db.commit()
        
        file_path = get_file_path(dataset.storage_path)
        df = parse_file(file_path, dataset.file_type or "text/csv")
        
        clean_result = clean_dataset(df)
        cleaned_df = clean_result["cleaned_df"]
        
        profile = profile_dataframe(cleaned_df)
        quality = calculate_quality_score(cleaned_df, profile)
        type_info = detect_type(cleaned_df.columns.tolist())
        
        dataset.dataset_type = type_info["dataset_type"]
        dataset.row_count = profile["overall"]["row_count"]
        dataset.column_count = profile["overall"]["column_count"]
        dataset.quality_score = quality["overall"]
        dataset.profile_json = profile
        dataset.cleaning_summary_json = clean_result["changes_log"]
        dataset.status = "ready"
        db.commit()
        
    except Exception as e:
        dataset.status = "failed"
        db.commit()
    finally:
        db.close()
