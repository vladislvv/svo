from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from db import SessionLocal
from schemas import OrderCreate, OrderResponse
from crud import create_order, mark_as_shipped
from calculator import calculate_price
import time

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/order", response_model=OrderResponse)
def create(order: OrderCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_order = create_order(db, order)
    print(f"[💳] Оплата прошла: заказ {new_order.id} на {new_order.price}")

    if new_order.is_paid == "yes":
        background_tasks.add_task(delayed_shipping, new_order.id)

    return new_order

@router.post("/calculate")
def calculate(order: OrderCreate):
    price = calculate_price(
        order.weight, order.width, order.height, order.length
    )
    return {"price": price}



def delayed_shipping(order_id: str):
    from db import SessionLocal
    db = SessionLocal()
    print(f" Ожидание 30 секунд перед отправкой заказа {order_id}...")
    time.sleep(30)
    try:
        mark_as_shipped(db, order_id)
        print(f" Заказ {order_id} был отправлен.")
    except Exception as e:
        print(f" Ошибка при автоотправке заказа {order_id}: {e}")
    finally:
        db.close()
