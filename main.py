from fastapi import FastAPI, Query, Depends, File, UploadFile
from datetime import datetime, timedelta, date, time
from models import ForkliftData
from database import get_db
from sqlalchemy.orm import Session
import json
from collections import defaultdict

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


@app.post("/analyze/distance_by_date_range/")
async def analyze_distance_by_date_range(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    data = db.query(ForkliftData).filter(ForkliftData.time >= start_date, ForkliftData.time <= end_date).all()

    grouped_data = defaultdict(list)
    for entry in data:
        key = (entry.time.date(), entry.forklift)
        grouped_data[key].append(entry)

    distance_by_day_and_forklift = defaultdict(int)
    for key, entries in grouped_data.items():
        for entry in entries:
            if entry.status == "ended" or entry.status == "reach":
                distance_by_day_and_forklift[key] += entry.distance

    result = {
        f"{key[0]} - Forklift {key[1]}": value for key, value in distance_by_day_and_forklift.items()
    }

    return result


@app.post("/analyze/orders_by_date_range/")
async def analyze_orders_by_date_range(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    data = db.query(ForkliftData).filter(ForkliftData.time >= start_date, ForkliftData.time <= end_date).all()

    # Группировка данные по дате и погрузчику
    grouped_data = defaultdict(list)
    for entry in data:
        key = (entry.time.date(), entry.forklift)
        grouped_data[key].append(entry)

    # Анализ количества выполненных заказов по дням и погрузчику
    orders_by_day_and_forklift = defaultdict(int)
    for key, entries in grouped_data.items():
        for entry in entries:
            if entry.status == "ended":
                orders_by_day_and_forklift[key] += 1

    result = {
        f"{key[0]} - Forklift {key[1]}": value for key, value in orders_by_day_and_forklift.items()
    }

    return result

@app.post("/analyze/time_moving_by_date_range/")
async def analyze_time_moving_by_date_range(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    data = db.query(ForkliftData).filter(ForkliftData.time >= start_date, ForkliftData.time <= end_date).all()

    grouped_data = defaultdict(list)
    for entry in data:
        key = (entry.time.date(), entry.forklift)
        grouped_data[key].append(entry)

    time_moving_by_day_and_forklift = defaultdict(lambda: timedelta(0))
    for key, entries in grouped_data.items():
        start_times = [entry.time for entry in entries if entry.status == "started"]
        end_times = [entry.time for entry in entries if entry.status == "ended"]

        if start_times and end_times:
            time_moving_by_day_and_forklift[key] += end_times[0] - start_times[0]

    result = {
        f"{key[0]} - Forklift {key[1]}": str(value) for key, value in time_moving_by_day_and_forklift.items()
    }

    return result


@app.post("/analyze/time_idle_by_date_range/")
async def analyze_time_idle_by_date_range(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    data = db.query(ForkliftData).filter(ForkliftData.time >= start_date, ForkliftData.time <= end_date).all()

    grouped_data = defaultdict(list)
    for entry in data:
        key = (entry.time.date(), entry.forklift)
        grouped_data[key].append(entry)

    total_day_time = timedelta(days=1)
    time_idle_by_day_and_forklift = defaultdict(lambda: total_day_time)

    time_moving_by_day_and_forklift = defaultdict(lambda: timedelta(0))
    for key, entries in grouped_data.items():
        start_times = [entry.time for entry in entries if entry.status == "started"]
        end_times = [entry.time for entry in entries if entry.status == "ended"]

        if start_times and end_times:
            time_moving_by_day_and_forklift[key] += end_times[0] - start_times[0]
            time_idle_by_day_and_forklift[key] -= time_moving_by_day_and_forklift[key]

    result = {
        f"{key[0]} - Forklift {key[1]}": str(value) for key, value in time_idle_by_day_and_forklift.items()
    }

    return result


@app.post("/analyze/time_in_status_by_forklift_and_date_range/")
async def analyze_time_in_status_by_forklift_and_date_range(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    # Получаем данные из базы для указанного периода
    data = db.query(ForkliftData).filter(ForkliftData.time >= start_date, ForkliftData.time <= end_date).order_by(ForkliftData.forklift, ForkliftData.time).all()

    time_in_status = defaultdict(lambda: defaultdict(lambda: timedelta(0)))
    previous_entries = {}

    for current_entry in data:
        forklift = current_entry.forklift
        if forklift in previous_entries:
            time_difference = current_entry.time - previous_entries[forklift].time
            time_in_status[forklift][previous_entries[forklift].status] += time_difference

        previous_entries[forklift] = current_entry

    end_datetime = datetime.combine(end_date, time(23, 59, 59))  # конец дня указанной даты
    for forklift, last_entry in previous_entries.items():
        time_difference = end_datetime - last_entry.time
        time_in_status[forklift][last_entry.status] += time_difference

    result = {
        forklift: {status: str(value) for status, value in status_data.items()}
        for forklift, status_data in time_in_status.items()
    }

    return result




