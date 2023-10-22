from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from report.services import *
from analyze.models import ForkliftData


router = APIRouter(
    prefix="/report",
    tags=["Отчеты"],
)

@router.get("/point_passes/", summary="Количество пересечений контрольных точек на складе")
async def point_passes_count_endpoint(db: Session = Depends(get_db), warehouse: int = Query(..., description="Номер склада")):
    return await point_passes_count(db, warehouse)


@router.get("/point_passes_by_forklift/", summary="Количество пересечений контрольных точек определенным погрузчиком")
async def point_passes_count_by_forklift_endpoint(forklift_id: int, db: Session = Depends(get_db), warehouse: int = Query(..., description="Номер склада")):    
    return await point_passes_count_by_forklift(db, forklift_id, warehouse)


@router.get("/broken_points/", summary="Не работающие контрольные точки")
async def broken_points_alert_endpoint(db: Session = Depends(get_db), warehouse: int = Query(..., description="Номер склада")):
    return await broken_points_alert(db, warehouse)
    

@router.get("/aggregate_forklift_data/", summary="Общие данные погрузчиков")
async def aggregate_forklift_data_endpoint(db: Session = Depends(get_db), warehouse: int = Query(..., description="Номер склада")):
    return await aggregate_forklift_data(db, warehouse)


@router.get("/order_info/{order_id}/", summary="Информация о заказе")
async def order_info_endpoint(order_id: int, db: Session = Depends(get_db)):
    data = db.query(ForkliftData).filter(ForkliftData.order == order_id).all()
    
    return {"order_data": [entry.__dict__ for entry in data]}


@router.get("/order_status/{order_id}/", summary="Статусы заказов")
async def order_status_endpoint(order_id: int, db: Session = Depends(get_db)):
    latest_status = db.query(ForkliftData.status).filter(ForkliftData.order == order_id).order_by(ForkliftData.time.desc()).first()
    
    return {"current_status": latest_status[0] if latest_status else None}


@router.get("/order_forklift/{order_id}/", summary="Погрузчик по заказу")
async def order_forklift_endpoint(order_id: int, db: Session = Depends(get_db)):
    forklift = db.query(ForkliftData.forklift).filter(ForkliftData.order == order_id).first()
    
    return {"forklift": forklift[0] if forklift else None}


@router.get("/order_duration/{order_id}/", summary="Длительность выполнения заказа")
async def order_duration_endpoint(order_id: int, db: Session = Depends(get_db)):
    return await order_duration(order_id, db)
