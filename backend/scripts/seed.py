import os
import sys
import uuid
import pandas as pd
from datetime import datetime, timezone

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember
from app.models.subscription import Subscription
from app.models.dataset import Dataset
from app.services.auth_service import hash_password
from app.services.ingestion.storage import save_file
from app.api.routes.datasets import process_dataset_synchronously

def seed():
    print("Seeding database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Create or get Demo User
        demo_email = "demo@datapilot.ai"
        user = db.query(User).filter(User.email == demo_email).first()
        if not user:
            user = User(
                id=uuid.uuid4(),
                name="Demo User",
                email=demo_email,
                password_hash=hash_password("DemoPassword123!"),
                role="admin",
                is_active=True
            )
            db.add(user)
            db.flush()
            print(f"Created demo user: {demo_email}")
        else:
            print(f"Demo user already exists: {demo_email}")

        # 2. Create or get Demo Workspace
        workspace = db.query(Workspace).filter(Workspace.owner_id == user.id).first()
        if not workspace:
            workspace = Workspace(
                id=uuid.uuid4(),
                name="Acme Corp Analytics",
                owner_id=user.id,
                brand_color="#4F46E5"
            )
            db.add(workspace)
            db.flush()
            
            member = WorkspaceMember(
                id=uuid.uuid4(),
                workspace_id=workspace.id,
                user_id=user.id,
                role="owner"
            )
            db.add(member)
            
            sub = Subscription(
                id=uuid.uuid4(),
                workspace_id=workspace.id,
                plan="pro",
                status="active"
            )
            db.add(sub)
            db.commit()
            print("Created demo workspace and Pro subscription")

        # 3. Seed Demo Sales Dataset if not exists
        sales_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'demo_sales.csv'))
        if os.path.exists(sales_csv_path):
            existing_ds = db.query(Dataset).filter(
                Dataset.workspace_id == workspace.id,
                Dataset.name == "Demo Sales 2023-2024"
            ).first()
            
            if not existing_ds:
                dest_dir = os.path.join("./uploads", str(workspace.id))
                os.makedirs(dest_dir, exist_ok=True)
                dest_filename = f"seed_sales_{uuid.uuid4().hex[:8]}.csv"
                dest_path = os.path.join(dest_dir, dest_filename)
                
                # Copy file
                import shutil
                shutil.copyfile(sales_csv_path, dest_path)
                
                rel_storage_path = f"{workspace.id}/{dest_filename}"
                
                dataset = Dataset(
                    id=uuid.uuid4(),
                    workspace_id=workspace.id,
                    uploaded_by=user.id,
                    name="Demo Sales 2023-2024",
                    original_filename="demo_sales.csv",
                    file_type="text/csv",
                    file_size=os.path.getsize(dest_path),
                    storage_path=rel_storage_path,
                    status="uploaded"
                )
                db.add(dataset)
                db.commit()
                db.refresh(dataset)
                
                # Run profiling & cleaning
                process_dataset_synchronously(dataset, db)
                print(f"Seeded and processed dataset: {dataset.name} (Quality Score: {dataset.quality_score}/100)")

        print("Database seeding completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()

