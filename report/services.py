from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from report.services import *
from analyze.models import ForkliftData


async def point_passes_count(db: Session):
    data = db.query(ForkliftData.point, func.count(ForkliftData.id)).group_by(ForkliftData.point).all()
    result = {point: count for point, count in data}

    return result

async def point_passes_count_by_forklift(db: Session, forklift_id: int):
    data = db.query(ForkliftData.point, func.count(ForkliftData.id)).filter(ForkliftData.forklift == forklift_id).group_by(ForkliftData.point).all()
    result = {point: count for point, count in data}
    
    return result

async def broken_points_alert(db: Session):
    threshold_time = datetime.now() - timedelta(hours=24)
    
    all_points = db.query(ForkliftData.point).distinct().all()
    all_points = [point[0] for point in all_points]
    
    last_passes = db.query(ForkliftData.point, func.max(ForkliftData.time)).group_by(ForkliftData.point).all()
    broken_points = [point for point, last_time in last_passes if last_time <= threshold_time]


    if broken_points:
        return {"alert": "Следующие контрольные точки не работают", "КТ": broken_points}
    else:
        return {"alert": "Все контрольные точки работают"}
    
async def aggregate_forklift_data(db: Session):
    total_passes = db.query(func.count(ForkliftData.id)).scalar()

    total_distance = db.query(func.sum(ForkliftData.distance)).scalar()

    min_time = db.query(func.min(ForkliftData.time)).scalar()
    max_time = db.query(func.max(ForkliftData.time)).scalar()
    if min_time and max_time:
        total_time = max_time - min_time
    else:
        total_time = None

    return {
        "Общее количество пересечения контрольных точек погрузчиками (шт)": total_passes,
        "Общее пройденное расстояние погрузчиками (км)": total_distance,
        "Общее время работы погрузчиков (сек)": total_time
    }

async def order_duration(order_id: int, db: Session):
    start_time = db.query(func.min(ForkliftData.time)).filter(ForkliftData.order == order_id).scalar()
    end_time = db.query(func.max(ForkliftData.time)).filter(ForkliftData.order == order_id).scalar()
    
    if start_time and end_time:
        duration = end_time - start_time
    else:
        duration = None

    return {"duration": str(duration)}
