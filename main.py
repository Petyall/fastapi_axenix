from fastapi import FastAPI, Query, Depends, File, UploadFile
from datetime import datetime, timedelta
from models import ForkliftData
from database import get_db
from sqlalchemy.orm import Session
import json


app = FastAPI()


@app.post("/import/")
async def import_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = await file.read()
    data = json.loads(file_content.decode("utf-8"))

    for item in data:
        item["time"] = datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S.%f")
        forklift_data = ForkliftData(**item)
        db.add(forklift_data)
        db.commit()

    return {"message": "Данные импортированы"}


@app.post("/analyze/")
async def analyze_data_endpoint(
        db: Session = Depends(get_db),  # зависимость для доступа к базе данных
        start_point: str = Query(..., description="Начальная контрольная точка (например, 'k1')"),
        end_point: str = Query(..., description="Конечная контрольная точка (например, 'k2')")
    ):
    time_differences = {}

    data = db.query(ForkliftData).filter((ForkliftData.point == start_point) | (ForkliftData.point == end_point)).all()

    previous_entry = None
    
    for entry in data:
        if (previous_entry and previous_entry.point == start_point and entry.point == end_point):
            current_time = entry.time
            time_difference = current_time - previous_entry.time
            
            # Создание ключа для пары точек (например, "k1-k2")
            key = f"{previous_entry.point}-{entry.point}"
            
            # Если ключ еще не существует в словаре, инициализируем его
            if key not in time_differences:
                time_differences[key] = []
            
            time_differences[key].append(time_difference)
                
        previous_entry = entry

    # Среднее время (прогноз)
    results = {}
    for key, values in time_differences.items():
        if key == f"{start_point}-{end_point}":
            average_time = sum(values, timedelta()).total_seconds() / len(values)
            results[key] = f"{average_time:.2f} секунд"
    
    return results
