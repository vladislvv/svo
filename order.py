# order.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import OrderCreate, OrderResponse
from db import SessionLocal
from crud import create_order
from calculator import calculate_price

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/order", response_model=OrderResponse)
def create(data: OrderCreate, db: Session = Depends(get_db)):
    new_order = create_order(db, data)
    print(f"[💳] Оплата прошла: заказ {new_order.id}, сумма {new_order.price}")
    return new_order

@router.post("/calculate")
def calculate(data: OrderCreate):
    price = calculate_price(
        weight=data.weight,
        width=data.width,
        height=data.height,
        length=data.length
    )
    return {"price": price}
