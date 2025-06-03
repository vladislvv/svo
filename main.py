from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import uuid

# ------------------ БД ------------------
DATABASE_URL = "postgresql://postgres:123123@localhost:5432/cargo_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ------------------ Модель ------------------
class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dot_a = Column(String, nullable=False)
    dot_b = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    status = Column(String, default="processing")
    price = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

# ------------------ Схемы ------------------
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

# ------------------ Калькулятор ------------------
def calculate_price(weight, width, height, length):
    base = 100
    volume = width * height * length / 1_000_000
    return round(base + (volume * 20000) + (weight * 150), 2)

# ------------------ FastAPI ------------------
app = FastAPI()

# ------------------ DB session ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ Роуты ------------------
@app.post("/order", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    price = calculate_price(order.weight, order.width, order.height, order.length)
    new_order = Order(**order.dict(), price=price)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    print(f"[💳] Оплата прошла: заказ {new_order.id} на {price}")
    return new_order

@app.get("/track/{order_id}")
def track_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {
        "id": order.id,
        "status": order.status,
        "from": order.dot_a,
        "to": order.dot_b,
        "price": order.price
    }

@app.post("/calculate")
def calculate(order: OrderCreate):
    price = calculate_price(order.weight, order.width, order.height, order.length)
    return {"price": price}
