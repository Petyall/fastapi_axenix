from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from analyze.services import *


router = APIRouter(
    prefix="/analyze",
    tags=["Аналитика"],
)


@router.post("/data_analyze/", summary="Прогонзирование времени прохождения КТ при ее поломке")
async def analyze_data_endpoint(
        db: Session = Depends(get_db),
        start_point: str = Query(..., description="Начальная контрольная точка (например, 'k1')"),
        end_point: str = Query(..., description="Конечная контрольная точка (например, 'k2')"),
        warehouse: int = Query(..., description="Номер склада"),
    ):
    return await analyze_data(db, start_point, end_point, warehouse)


@router.post("/distance_by_date_range/", summary="Пройденное расстояние погрузчиком за период времени")
async def analyze_distance_by_date_range_endpoint(
    db: Session = Depends(get_db),
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    warehouse: int = Query(..., description="Номер склада"),
):
    return await analyze_distance_by_date_range(db, start_date, end_date, warehouse)


@router.post("/orders_by_date_range/", summary="Количество выполненных заказов погрузчиками за пероид времени")
async def analyze_orders_by_date_range_endpoint(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db),
    warehouse: int = Query(..., description="Номер склада")  
):
    return await analyze_orders_by_date_range(db, start_date, end_date, warehouse)


@router.post("/time_moving_by_date_range/", summary="Время погрузчиков в работе за период времени")
async def analyze_time_moving_by_date_range_endpoint(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db),
    warehouse: int = Query(..., description="Номер склада")
):
    return await analyze_time_moving_by_date_range(db, start_date, end_date, warehouse)


@router.post("/time_idle_by_date_range/", summary="Время погрузчиков в бездействии за период времени")
async def analyze_time_idle_by_date_range_endpoint(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db),
    warehouse: int = Query(..., description="Номер склада")
):
    return await analyze_time_idle_by_date_range(db, start_date, end_date, warehouse)


@router.post("/time_in_status_by_forklift_and_date_range/", summary="Общее время в каждом из статусов погрузчиков за период времени")
async def analyze_time_in_status_by_forklift_and_date_range_endpoint(
    start_date: date = Query(..., description="Дата начала периода анализа"),
    end_date: date = Query(..., description="Дата окончания периода анализа"),
    db: Session = Depends(get_db),
    warehouse: int = Query(..., description="Номер склада")
):
    return await analyze_time_in_status_by_forklift_and_date_range(db, start_date, end_date, warehouse)
