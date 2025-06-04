from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from crud import pay_for_order

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pay")
def pay(order_id: str, db: Session = Depends(get_db)):
    result = pay_for_order(db, order_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    if result == "already_paid":
        raise HTTPException(status_code=400, detail="Заказ уже оплачен")
    return {"message": f"Оплата прошла успешно для заказа {order_id}", "status": result.status}
