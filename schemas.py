from pydantic import BaseModel

class OrderCreate(BaseModel):
    dot_a: str
    dot_b: str
    weight: float
    width: float
    height: float
    length: float


class OrderResponse(OrderCreate):
    id: str
    status: str
    price: float
