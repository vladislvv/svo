from sqlalchemy import Column, String, Float
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
    price = Column(Float,nullable=False)

