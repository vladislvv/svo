# main.py
from fastapi import FastAPI
from order import router as order_router
from tracking import router as tracking_router
from models import Base
from db import engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Подключаем маршруты
app.include_router(order_router)
app.include_router(tracking_router)
