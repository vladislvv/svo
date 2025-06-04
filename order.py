# order.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from schemas import OrderCreate, OrderResponse
from crud import create_order, mark_as_shipped, get_order_by_id
from calculator import calculate_price

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/order", response_model=OrderResponse)
def create(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = create_order(db, order)
    print(f"[💳] Оплата прошла: заказ {new_order.id} на {new_order.price}")
    return new_order

@router.post("/calculate")
def calculate(order: OrderCreate):
    price = calculate_price(
        order.weight, order.width, order.height, order.length
    )
    return {"price": price}

@router.post("/ship/{order_id}")
def ship(order_id: str, db: Session = Depends(get_db)):
    shipped_order = mark_as_shipped(db, order_id)
    return {"message": f"Заказ {order_id} отправлен.", "status": shipped_order.status}

@router.get("/track/{order_id}")
def track(order_id: str, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)
    if not order:
        return {"error": "Заказ не найден"}
    return {
        "id": order.id,
        "status": order.status,
        "is_paid": order.is_paid,
        "from": order.dot_a,
        "to": order.dot_b,
        "price": order.price,
        "cooling": order.cooling,
        "insurance": order.insurance,
        "loaders": order.loaders,
        "passenger_space": order.passenger_space,
        "escort": order.escort,
        "airline": order.airline
    }
