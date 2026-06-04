from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    date = Column(DateTime, index=True)
    product_name = Column(String, index=True)
    category = Column(String, index=True)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)
    customer_id = Column(String, index=True)
    region = Column(String, index=True)
    segment = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class KPICache(Base):
    """Optional: Cache for pre-calculated KPIs to improve performance"""
    __tablename__ = "kpi_cache"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, index=True)
    metric_value = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    filters = Column(String)  # JSON string of applied filters
    updated_at = Column(DateTime, default=datetime.utcnow)
