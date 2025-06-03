from fastapi import FastAPI
from db import engine
from models import Base
from order import router as order_router
from tracking import router as tracking_router
from airlines import router as airline_router
from payment import router as payment_router



app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(order_router)
app.include_router(tracking_router)
app.include_router(airline_router)
app.include_router(payment_router)

