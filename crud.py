# crud.py
from sqlalchemy.orm import Session
from models import Order
from schemas import OrderCreate
from calculator import calculate_price

def create_order(db: Session, order_data: OrderCreate):
    price = calculate_price(
        weight=order_data.weight,
        width=order_data.width,
        height=order_data.height,
        length=order_data.length
    )
    db_order = Order(**order_data.dict(), price=price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()
