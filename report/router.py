from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from report.services import *
from analyze.models import ForkliftData


router = APIRouter(
    prefix="/report",
    tags=["Отчеты"],
)

@router.get("/point_passes/")
async def point_passes_count(db: Session = Depends(get_db)):
    data = db.query(ForkliftData.point, func.count(ForkliftData.id)).group_by(ForkliftData.point).all()
    result = {point: count for point, count in data}
    
    return result


@router.get("/point_passes_by_forklift/")
async def point_passes_count_by_forklift(forklift_id: int, db: Session = Depends(get_db)):
    data = db.query(ForkliftData.point, func.count(ForkliftData.id)).filter(ForkliftData.forklift == forklift_id).group_by(ForkliftData.point).all()
    result = {point: count for point, count in data}
    
    return result


@router.get("/broken_points/")
async def broken_points_alert(db: Session = Depends(get_db)):
    threshold_time = datetime.now() - timedelta(hours=24)
    
    all_points = db.query(ForkliftData.point).distinct().all()
    all_points = [point[0] for point in all_points]
    
    last_passes = db.query(ForkliftData.point, func.max(ForkliftData.time)).group_by(ForkliftData.point).all()
    broken_points = [point for point, last_time in last_passes if last_time <= threshold_time]

    if broken_points:
        return {"alert": "Следующие контрольные точки не работают", "КТ": broken_points}
    else:
        return {"alert": "Все контрольные точки работают"}
    

@router.get("/aggregate_forklift_data/")
async def aggregate_forklift_data(db: Session = Depends(get_db)):
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


@router.get("/order_info/{order_id}/")
async def order_info(order_id: int, db: Session = Depends(get_db)):
    data = db.query(ForkliftData).filter(ForkliftData.order == order_id).all()
    
    return {"order_data": [entry.__dict__ for entry in data]}


@router.get("/order_status/{order_id}/")
async def order_status(order_id: int, db: Session = Depends(get_db)):
    latest_status = db.query(ForkliftData.status).filter(ForkliftData.order == order_id).order_by(ForkliftData.time.desc()).first()
    
    return {"current_status": latest_status[0] if latest_status else None}


@router.get("/order_forklift/{order_id}/")
async def order_forklift(order_id: int, db: Session = Depends(get_db)):
    forklift = db.query(ForkliftData.forklift).filter(ForkliftData.order == order_id).first()
    
    return {"forklift": forklift[0] if forklift else None}


@router.get("/order_duration/{order_id}/")
async def order_duration(order_id: int, db: Session = Depends(get_db)):
    start_time = db.query(func.min(ForkliftData.time)).filter(ForkliftData.order == order_id).scalar()
    end_time = db.query(func.max(ForkliftData.time)).filter(ForkliftData.order == order_id).scalar()
    
    if start_time and end_time:
        duration = end_time - start_time
    else:
        duration = None

    return {"duration": str(duration)}
