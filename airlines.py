from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Airline
from schemas import AirlineResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/airlines", response_model=list[AirlineResponse])
def list_airlines(db: Session = Depends(get_db)):
    return db.query(Airline).all()
