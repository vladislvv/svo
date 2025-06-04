from pydantic import BaseModel

class OrderCreate(BaseModel):
    dot_a: str
    dot_b: str
    weight: float
    width: float
    height: float
    length: float
    cooling: bool = False
    insurance: bool = False
    loaders: bool = False
    passenger_space: bool = False
    escort: bool = False
    airline: str = None

class OrderResponse(OrderCreate):
    id: str
    status: str
    price: float
    is_paid: str




class AirlineResponse(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True
