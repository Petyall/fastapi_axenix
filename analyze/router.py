from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from analyze.services import *


router = APIRouter(
    prefix="/analyze",
    tags=["Аналитика"],
)


@router.post("/data_analyze/")
async def analyze_data_endpoint(
        db: Session = Depends(get_db),
        start_point: str = Query(..., description="Начальная контрольная точка (например, 'k1')"),
        end_point: str = Query(..., description="Конечная контрольная точка (например, 'k2')")
    ):
    return await analyze_data(db, start_point, end_point)


@router.post("/distance_by_date_range/")
async def analyze_distance_by_date_range_endpoint(
    db: Session = Depends(get_db),
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа")    
):
    return await analyze_distance_by_date_range(db, start_date, end_date)


@router.post("/orders_by_date_range/")
async def analyze_orders_by_date_range_endpoint(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    return await analyze_orders_by_date_range(db, start_date, end_date)


@router.post("/time_moving_by_date_range/")
async def analyze_time_moving_by_date_range_endpoint(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    return await analyze_time_moving_by_date_range(db, start_date, end_date)


@router.post("/time_idle_by_date_range/")
async def analyze_time_idle_by_date_range_endpoint(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    return await analyze_time_idle_by_date_range(db, start_date, end_date)


@router.post("/time_in_status_by_forklift_and_date_range/")
async def analyze_time_in_status_by_forklift_and_date_range_endpoint(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db)
):
    return await analyze_time_in_status_by_forklift_and_date_range(db, start_date, end_date)
