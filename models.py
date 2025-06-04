from sqlalchemy import Column, String, Float, Boolean
from db import Base
import uuid

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
    is_paid = Column(String, default="no")
    cooling = Column(Boolean, default=False)
    insurance = Column(Boolean, default=False)
    loaders = Column(Boolean, default=False)
    passenger_space = Column(Boolean, default=False)
    escort = Column(Boolean, default=False)
    airline = Column(String, nullable=True)



class Airline(Base):
    __tablename__ = "airlines"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
is_paid = Column(String, default="no")
