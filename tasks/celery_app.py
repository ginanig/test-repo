# tasks/celery_app.py
from celery import Celery
import os
from dotenv import load_dotenv

# load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://eeg_user:eeg_password@localhost:5432/eeg_platform") 

app = Celery(
    "tasks", 
    broker=REDIS_URL,
    backend=REDIS_URL, 
    include=["tasks.edf_tasks"] 
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    app.start()
