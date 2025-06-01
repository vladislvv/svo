# tracking.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from crud import get_order_by_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/track/{order_id}")
def track_order(order_id: str, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {
        "id": order.id,
        "status": order.status,
        "from": order.dot_a,
        "to": order.dot_b,
        "price": order.price
    }
