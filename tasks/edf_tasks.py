# tasks/edf_tasks.py
from .celery_app import app
import time
import random
# import mne 
# from sqlalchemy.orm import Session 
# from backend.app.core.database import SessionLocal, engine 
# from backend.app.edf_uploads.models import EdfFileMetadata 

@app.task(bind=True, name="process_edf_file")
def process_edf_file(self, edf_file_metadata_id: int, s3_key: str):
    task_id = self.request.id
    print(f"[{task_id}] Iniciando processamento para EdfFileMetadata ID: {edf_file_metadata_id}, S3 Key: {s3_key}")

    total_steps = 4
    current_step = 0

    current_step += 1
    self.update_state(state='PROGRESS', meta={'current': current_step, 'total': total_steps, 'status': f'Carregando arquivo {s3_key}...' })
    print(f"[{task_id}] Etapa 1/4: Carregando arquivo {s3_key} (simulação)...")
    time.sleep(random.randint(5, 10)) 

    current_step += 1
    self.update_state(state='PROGRESS', meta={'current': current_step, 'total': total_steps, 'status': 'Aplicando filtros...'})
    print(f"[{task_id}] Etapa 2/4: Aplicando filtros (simulação)...")
    time.sleep(random.randint(3, 7))

    current_step += 1
    self.update_state(state='PROGRESS', meta={'current': current_step, 'total': total_steps, 'status': 'Aplicando ICA...'})
    print(f"[{task_id}] Etapa 3/4: Aplicando ICA (simulação)...")
    time.sleep(random.randint(5, 10))

    current_step += 1
    self.update_state(state='PROGRESS', meta={'current': current_step, 'total': total_steps, 'status': 'Extraindo potências de bandas...'})
    print(f"[{task_id}] Etapa 4/4: Extraindo potências de bandas (simulação)...")
    simulated_band_powers = {
        "delta": random.uniform(10, 30),
        "theta": random.uniform(5, 20),
        "alpha": random.uniform(2, 15),
        "beta": random.uniform(1, 10),
        "gamma": random.uniform(0.5, 5)
    }
    print(f"[{task_id}] Potências de bandas (simuladas): {simulated_band_powers}")
    time.sleep(random.randint(2, 5))

    return {"status": "Success", "message": "EDF file processed successfully (simulated).", "band_powers": simulated_band_powers}

@app.task(name="example_task")
def example_task(x, y):
    time.sleep(2) 
    return x + y
