from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class ForkliftData(Base):
    __tablename__ = "forklift_data"

    id = Column(Integer, primary_key=True, index=True)
    order = Column(Integer, index=True)
    forklift = Column(Integer, index=True)
    warehouse = Column(Integer)
    status = Column(String)
    point = Column(String)
    distance = Column(Integer)
    time = Column(DateTime)
