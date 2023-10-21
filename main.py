from fastapi import FastAPI, Depends, File, UploadFile
from datetime import datetime
from database import get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from report.router import router as router_report
from analyze.router import router as router_analyze
from analyze.models import ForkliftData

import json

app = FastAPI()

origins = ["https://89.108.65.56"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
)

app.include_router(router_analyze)
app.include_router(router_report)

# @app.post("/import/")
# async def import_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     file_content = await file.read()
#     data = json.loads(file_content.decode("utf-8"))

#     for item in data:
#         item["time"] = datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S.%f")
#         forklift_data = ForkliftData(**item)
#         db.add(forklift_data)
#         db.commit()

#     return {"message": "Данные импортированы"}
