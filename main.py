from fastapi import FastAPI, Depends, File, UploadFile
from datetime import datetime
from database import get_db
from sqlalchemy.orm import Session

from analyze.router import router as router_analyze
from analyze.models import ForkliftData

import json


app = FastAPI()

app.include_router(router_analyze)

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
