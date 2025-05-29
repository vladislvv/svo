from fastapi import FastAPI
from db import engine
from models import Base
from order import router as order_router
from tracking import router as tracking_router

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(order_router, tags=["Order"])
app.include_router(tracking_router, tags=["Tracking"])
