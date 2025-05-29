from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from schemas import OrderCreate, OrderResponse
from crud import create_order

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/order", response_model=OrderResponse)
def create_order_route(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)
