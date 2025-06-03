from sqlalchemy.orm import Session
from models import Order
from schemas import OrderCreate
from calculator import calculate_price
from fastapi import HTTPException

def create_order(db: Session, order_data: OrderCreate):
    price = calculate_price(
        order_data.weight,
        order_data.width,
        order_data.height,
        order_data.length
    )
    db_order = Order(**order_data.dict(), price=price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()


def pay_for_order(db: Session, order_id: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    if order.is_paid == "yes":
        return "already_paid"

    order.is_paid = "yes"
    order.status = "paid"
    db.commit()
    db.refresh(order)
    return order


def mark_as_shipped(db: Session, order_id: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    if order.is_paid != 'yes':
        raise HTTPException(status_code=400, detail="Заказ ещё не оплачен")
    order.status = "shipped"
    db.commit()
    db.refresh(order)
    return order

