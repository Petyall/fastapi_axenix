from pydantic import BaseModel

class DataItem(BaseModel):
    Order: int
    Forklift: int
    Warehouse: int
    Status: str
    Point: str
    Distance: int
    Time: str